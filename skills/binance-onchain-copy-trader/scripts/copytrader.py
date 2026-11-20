#!/usr/bin/env python3
"""On-chain copy-trading daemon for Binance Agentic Wallet. DRY-RUN ONLY.

Live-trading code was REMOVED from this script 2026-11-19 (Papao); it cannot
place real orders. Any mode value other than "dry-run" refuses startup.

Sources:   baw tracker ws --address-list / --smy (read-only event stream)
Execution (dry-run only): audit ∥ live price (concurrent) -> simulated fill;
no order is ever placed, and no protective order exists.

DISCLAIMER
    This is a scaffold, not a trading product, and it carries no strategy. The
    bundled hooks are a minimal reference implementation with no evidence of
    positive expectancy. Every risk control, position-management scheme and
    parameter value here is a suggestion, not a safeguard: the daemon runs the
    checks you configure and does not judge whether they are sufficient.

    Nothing here is investment advice. On-chain transactions are irreversible,
    and automated trading can lose money through market conditions you did not
    anticipate, changes in platform behavior, or defects in this software. It is
    provided as-is, without warranty of any kind. You are solely responsible for
    what you run and for any funds you commit.
"""
import json, os, queue, subprocess, threading, time, uuid, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

# The code lives in the skill directory; runtime data goes to ~/.local/copytrader
# (override with COPYTRADER_HOME). The skill directory holds the skill only —
# no logs, no state, no archives.
D = os.path.expanduser(os.environ.get("COPYTRADER_HOME", "~/.local/copytrader"))
os.makedirs(D, exist_ok=True)
CFG_F, ST_F = f"{D}/config.json", f"{D}/state.json"
LOG_F, EVJ, ORDJ = f"{D}/copytrader.log", f"{D}/events.jsonl", f"{D}/orders.jsonl"
OUTJ = f"{D}/outcomes.jsonl"
STOP_F, KILL_F = f"{D}/STOP", f"{D}/KILL"
LOCK_F = f"{D}/copytrader.lock"
# REMOVED 2026-11-19 (Papao): the acknowledgement file for live trading and
# the confirmation gate were deleted from this script. Live trading is
# technically impossible here; see SKILL.md "MODIFIKASI KEAMANAN".

# Protocol sentinel for the chain's native token (not a wallet) — the same
# constant the wallet CLI and binance-agentic-wallet use.
NATIVE = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
AUDIT_URL = "https://web3.binance.com/bapi/defi/v1/public/wallet-direct/security/token/audit"
PRICE_URL = ("https://web3.binance.com/bapi/defi/v4/public/wallet-direct/buw/"
             "wallet/market/token/dynamic/info/ai?chainId={c}&contractAddress={a}")
UA = {"Accept-Encoding": "identity", "User-Agent": "binance-onchain-copy-trader"}

# Only plumbing parameters that cannot affect capital safety get defaults.
# Chain, quote token, resource guardrails and every strategy parameter have
# **no defaults** — a missing one refuses startup. Reason: once such a value is
# defaulted, an operator can end up committing real money to a number they never
# thought about. The single exception is `mode`: absent means dry-run, so an
# omission can never silently become live trading.
DEFAULTS = dict(
    mode="dry-run",             # the ONLY accepted value; anything else refuses startup
    address_list="addrs.txt",   # filename only; you still supply the contents
    policy={},                  # passed verbatim to the strategy hooks; keys are not interpreted here
    reconcile_sec=60,
    proc_restart_sec=10,        # delay before restarting an exited child. Connection-level
                                # reconnect is the CLI's job, not ours
    workers=4,
    # Outcome sampling. After every decision that WOULD have opened a position
    # (including dry-run, where nothing is bought), re-read the price at these
    # horizons and append the result to outcomes.jsonl. This is what makes
    # "test your features against outcomes" actually possible without spending
    # money — events.jsonl on its own records the decision but not whether it
    # was right. Set to [] to switch off.
    outcome_horizons_min=[5, 15, 60],
)

# Must be given explicitly in config.json, or startup is refused.
REQUIRED_CFG = ["chain", "quote_token", "sources",
                "budget_usd", "position_usd", "max_positions", "gas_floor_native"]

# Strategy parameters the reference hooks read. Replace the hooks and this list
# changes with them — the mechanism layer does not care what these keys mean, it
# only blocks startup when one is missing, so that a hook never quietly uses a
# value the operator never decided on.
REQUIRED_POLICY = ["follow_sides", "max_event_age_sec",
                   "sl_mult", "tp_mult", "tp_fraction",
                   "buy_slippage", "sl_slippage", "tp_slippage"]

# ══════════════════════════════════════════════════════════════════
#  STRATEGY HOOKS — this block is yours to edit; the mechanism layer never
#  touches it.
#
#  The three hooks decide "enter or not, how much, and how to exit". The
#  mechanism layer delivers events here, executes your decisions, and enforces
#  the resource guardrails.
#
#  ev   normalized event; fields are documented in SKILL.md "Event schema"
#  ctx  context: {audit, liquidity, price, positions, deployed, cfg, policy}
# ══════════════════════════════════════════════════════════════════

def should_enter(ev, ctx):
    """Decide whether to open a position. Returns (bool, reason).

    Called TWICE: the first time ctx["audit"] / ctx["liquidity"] are None (before
    any request is issued, so only zero-cost checks are possible); the second
    time after that data has been fetched.

    Available signals (all may be None — check before use):
      ev["side"]  11/19 = buy, 21/29 = sell   ev["ts"]  counterparty fill time
      ev["price"] entry reference price       ev["usd"] counterparty's USD size
      ev["top10"] top-10 holder concentration ev["tags"] token tags
      ev["extra"] source-specific (signal stream: smy/exitRate/status/liq)
      ctx["audit"] raw audit response         ctx["liquidity"] liquidity
      ctx["positions"] open positions         ctx["policy"] the `policy` section of config.json

    ── The implementation below is a minimal reference that runs, NOT a
       recommended strategy ──
    It deliberately makes very few judgements, because "which features actually
    predict anything" has to be tested against your own events.jsonl rather than
    copied. Things worth knowing while you design yours:

      · A liquidity floor is meaningful on the address stream; on the signal
        stream it is close to a no-op — the signal source already filters on
        liquidity, so nearly everything passes. Do not rely on it to do your
        filtering.
      · `riskLevel == 0` does not mean "confirmed safe"; it can also mean "not
        yet assessed" (in which case riskLevelEnum is empty). Treating it as an
        allowlist lets unassessed tokens through as if they were safe.
      · Intuitions like "a bigger counterparty buy is more trustworthy" or
        "lower top-10 concentration is better" often do not hold for newly
        launched tokens; thresholds set by feel reject most legitimate candidates.
      · Waiting for "several addresses to agree" costs you the price movement
        during the wait — the later consensus is confirmed, the worse your entry.
        If you want it, first measure how late the second address typically is.
      · Over-rejection looks exactly like "no signals". Before adding any gate,
        make sure you can see what it rejected in the `decision` distribution of
        events.jsonl.
    """
    p = ctx["policy"]
    # ---- Direction / status gate (zero cost, catchable on the first call) ----
    if ev["src"] == "address":
        if ev["side"] not in p["follow_sides"]:
            return False, f"side={ev['side']}"
    else:
        # `status` is usually null on the first push (the documentation is
        # explicit: only lifecycle states such as timeout / exitRate /
        # outDecline are stamped on later pushes). So only "explicitly bad"
        # states may be rejected and a missing value MUST pass — writing
        # `if st not in (...)` silently drops almost every genuine first push,
        # and the symptom is identical to "this chain has no signals", which
        # makes it very hard to diagnose.
        # Expired timeout re-pushes do carry a status and have an old
        # signalTriggerTime, so the freshness gate below catches them.
        st = ev["extra"].get("status")
        if st is not None and st not in ("valid", "active"):
            return False, f"status={st}"
        # Do NOT use exitRate / maxGain / currentPrice for entry decisions here.
        # They describe how a signal evolved after it fired; the server has not
        # computed them at first-push time, and the documentation
        # (binance-wallet-tracker, "Signal field nullability") confirms they are
        # usually null on first push. A threshold gate on them never fires on a
        # first push and only misjudges older signals joined mid-life. Use them
        # for exit logic or post-hoc analysis — the fields are still logged.

    # ---- Delivery freshness ----
    #      signalTriggerTime is now reliably carried on the signal stream's first
    #      push, so it can be used directly to compute delivery latency. A null
    #      ts still passes, so that an occasional omission does not wipe out a
    #      whole batch.
    max_age = p.get("max_event_age_sec")
    if max_age and ev["ts"] and (time.time() - ev["ts"]) > max_age:
        return False, f"stale {time.time()-ev['ts']:.0f}s"

    # ---- On the first call the enrichment data is not ready; the zero-cost
    #      checks are done, so pass and wait for the second call ----
    if not ctx.get("enriched"):
        return True, "ok(pending enrichment)"

    # Liquidity does not depend on the audit. On the address stream it comes from
    # market data; on the signal stream from the event's own alertLiquidity
    # (reliably present on first push). Note the signal source already filters on
    # liquidity, so this gate is close to a no-op there.
    liq = ctx.get("liquidity")
    if liq is None:
        if p.get("require_liquidity_known", True):
            return False, "liquidity unknown"
    else:
        lo = p.get("min_liquidity_usd")
        if lo and liq < lo:
            return False, f"liquidity ${liq:,.0f}<${lo:,.0f}"

    # ---- Everything below needs the audit. If this source does not fetch one
    #      (see policy.enrich_srcs), skip it. ----
    a = ctx.get("audit")
    if a is None:
        return True, "ok(no audit fetched)"

    bl = p.get("block_risk_levels") or []
    try:    rl = int(a.get("riskLevel"))
    except Exception: rl = None
    if rl is not None and rl in bl:
        return False, f"riskLevel={rl}"

    cap = p.get("max_sell_tax_pct")
    if cap is not None:
        try:    stax = float((a.get("extraInfo") or {}).get("sellTax") or 0) * 100
        except Exception: stax = 0.0
        if stax > cap:
            return False, f"sellTax {stax:.1f}%>{cap}%"

    return True, "ok"

def size_position(ev, ctx):
    """Decide how many USD to commit. Return a float; 0 means skip.
    The mechanism layer then clamps to min(value, position_usd, remaining budget)."""
    return ctx["cfg"]["position_usd"]

def exit_plan(ev, ctx, entry_price, qty):
    """Decide which protective orders to place. Return a list of
    (trigger_price, sell_qty, slippage_pct); they are placed in the order
    returned, so put the most important one first (usually the stop-loss).
    Returning an empty list places no protection at all.

    Note: the structure below (stop-loss first, take-profit on part of the
    position) is a SUGGESTED shape, not a requirement. If you return an empty
    list the mechanism layer will not add protection on your behalf.
    """
    p = ctx["policy"]
    # These keys are guaranteed present by the startup check (REQUIRED_POLICY),
    # so they are read directly — deliberately with no fallback default: a
    # stop-loss distance the operator never decided on must never be used quietly.
    sl_mult, tp_mult = p["sl_mult"], p["tp_mult"]
    tp_frac = p["tp_fraction"]
    plan = []
    if sl_mult: plan.append((entry_price * sl_mult, qty, p["sl_slippage"]))
    if tp_mult: plan.append((entry_price * tp_mult, qty * tp_frac, p["tp_slippage"]))
    return plan

# ══════════════════════════════════════════════════════════════════

def now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
_lk = threading.Lock()
def log(*a):
    line = f"[{now()}] " + " ".join(str(x) for x in a)
    with _lk:
        print(line, flush=True)
        try:
            with open(LOG_F, "a") as f: f.write(line + "\n")
        except Exception: pass

# Template written on the first run. **Everything is left empty** — deliberately
# no directly runnable numbers, because values like stop-loss distance and
# per-trade size have to be the result of the operator's own decision rather
# than something copied. Each field's meaning and how to choose it are in
# SKILL.md; fill them in before starting.
CFG_TEMPLATE = dict(
    mode="dry-run",
    chain=None,                 # `baw wallet chains --json` for currently supported chains
    quote_token=None,           # quote-token contract address on that chain, **lowercase**
    sources=None,               # ["address"] / ["signal"] / both
    budget_usd=None,            # cumulative deployment cap (no reinvestment; only grows)
    position_usd=None,          # per-trade size
    max_positions=None,         # concurrent position cap
    gas_floor_native=None,      # stop opening below this native balance; also stop if unreadable
    policy=dict(
        follow_sides=None,      # which tradeSideCategory values to follow on the address stream
        max_event_age_sec=None, # delivery freshness ceiling, seconds
        sl_mult=None,           # stop-loss trigger = entry price × this
        tp_mult=None,           # take-profit trigger = entry price × this
        tp_fraction=None,       # fraction of the position sold at take-profit
        buy_slippage=None,      # entry slippage tolerance (%)
        sl_slippage=None,       # stop-loss slippage (%) — a stop that cannot fill in a
                                # crash is not protection, so keep this wider than tp
        tp_slippage=None,       # take-profit slippage tolerance (%)
        block_honeypot=True,    # honeypot block. On by default; disabling is not advised
        require_audit=False,    # reject when the audit returns no result?
    ))

def load_cfg():
    """Precedence: DEFAULTS < config.json. Whatever the file says, wins."""
    c = dict(DEFAULTS)
    user = {}
    if os.path.exists(CFG_F):
        try: user = json.load(open(CFG_F))
        except Exception as e: log("!! failed to parse config.json, using defaults:", e)
    else:
        json.dump(CFG_TEMPLATE, open(CFG_F, "w"), indent=1, ensure_ascii=False)
        user = dict(CFG_TEMPLATE)
        log(f"wrote config template {CFG_F} — every field is empty; fill it in before starting. See SKILL.md")
    for k, v in user.items():                      # user config applies last and always wins
        if isinstance(v, dict) and isinstance(c.get(k), dict): c[k] = {**c[k], **v}
        else: c[k] = v
    return c

CFG = load_cfg()

# LIVE TRADING REMOVED (Papao, 2026-11-19): only "dry-run" is accepted. Any
# other value refuses startup outright — it is NOT silently converted to a
# test run, so a stale config can never be misread as harmless.
if CFG.get("mode") != "dry-run":
    raise SystemExit("LIVE TRADING REMOVED 2026-11-19: this script is dry-run "
                     "only; refusing to start.")

def check_cfg(c):
    """A missing field refuses startup; nothing falls back to a default.

    Resource guardrails and strategy parameters have no safe defaults — a
    stop-loss distance the operator never decided on is exactly as dangerous as
    a position size they never decided on. Better not to start at all than to
    commit real money using someone else's numbers. (`mode` is the one
    exception: absent means dry-run, which fails in the safe direction.)
    """
    missing = [k for k in REQUIRED_CFG if c.get(k) in (None, "", [])]
    pol = c.get("policy") or {}
    missing += [f"policy.{k}" for k in REQUIRED_POLICY if pol.get(k) is None]
    return missing

PROC_RESTART_SEC = int(CFG.get("proc_restart_sec") or 10)

# Lowercase every address. Chains differ in how strictly they validate address
# format: some accept EIP-55 mixed case, others reject it outright with
#   "[20003002] Invalid fromToken address"
# Lowercase works everywhere. Note how this failure presents: every order on the
# affected leg fails, and "never filling anything" is indistinguishable from
# "this chain has no signals" in every liveness metric — unless failed orders
# are counted explicitly, it can hide for a long time.
if isinstance(CFG.get("quote_token"), str):
    CFG["quote_token"] = CFG["quote_token"].lower()

def load_state():
    if os.path.exists(ST_F):
        try: return json.load(open(ST_F))
        except Exception: pass
    return {"deployed": 0.0, "pos": {}, "handled": [], "runs": 0, "last_event_ms": None}
S = load_state()
SAVE_LK = threading.Lock()
OPENING_LK = threading.Lock()
FOLLOWUP_LK = threading.Lock()   # guards S["followups"]; see followup_worker
_LOCK_FD = None                  # single-instance flock fd; must stay open
OPENING = set()   # contract addresses currently being opened; guards the same-token race
# Liveness metric: last_event_ms is written after deduplication, so it only
# reflects NEW signalIds and re-pushes never update it — during a quiet market it
# looks like a dead stream. LAST_PUSH / PUSHES record every push and are the real
# evidence that the connection is alive.
LAST_PUSH = [0.0]
PUSHES = [0]
# Order failures must be counted and persisted separately: a leg that "never
# fills anything" and a leg where "a config error makes every order fail" look
# identical in every liveness metric.
FAILS = [0]
QUOTE_MARK = [None]      # last known quote-token balance
# REMOVED 2026-11-19 (Papao): the closed-position ledger (LEDGER_F) and
# ledger_add() were deleted with the live-trading flow they served. In
# dry-run mode no position is ever opened or closed, so there is nothing to
# ledger.
# REMOVED 2026-11-19 (Papao): ledger_add() deleted with the live-trading flow
# it served. In dry-run mode no position is ever opened or closed, so there is
# nothing to ledger. Any stale caller fails with NameError (intentional).

def save():
    """state.json is the budget and position ledger, so writes must be
    serialized: when several workers share one temp filename, the second
    os.replace raises FileNotFoundError because the first already moved the file
    away, and the accounting write is lost."""
    with SAVE_LK:
        t = f"{ST_F}.{os.getpid()}.{threading.get_ident()}.tmp"
        try:
            with open(t, "w") as f:
                json.dump(S, f, indent=1, default=str)
            os.replace(t, ST_F)
        finally:
            if os.path.exists(t):
                try: os.remove(t)
                except OSError: pass

# REMOVED 2026-11-19 (Papao): add_deployed() deleted. It only ever ran inside
# the deleted live branch of open_position(). Any stale caller fails with
# NameError (intentional).

def jsonl(path, row):
    try:
        with open(path, "a") as f: f.write(json.dumps(row, default=str) + "\n")
    except Exception: pass

def fnum(v, d=None):
    try: return float(v)
    except Exception: return d

# ---------------- CLI / HTTP ----------------
def baw(*args, timeout=180):
    try:
        p = subprocess.run(["baw", *args, "--json"], capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, {"message": "timeout"}
    out = (p.stdout or p.stderr or "").strip()
    i = out.find("{")
    if i < 0: return False, {"message": out[:200] or "no output"}
    try: j = json.loads(out[i:])
    except Exception: return False, {"message": out[:200]}
    return bool(j.get("success")), (j.get("data") if j.get("success") else j.get("error", {}))

def http_json(url, body=None, extra=None, timeout=20):
    h = dict(UA)
    if extra: h.update(extra)
    data = None
    if body is not None:
        data = json.dumps(body).encode(); h["Content-Type"] = "application/json"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h), timeout=timeout) as r:
            return json.load(r)
    except Exception:
        return None

def audit(ca):
    r = http_json(AUDIT_URL, {"binanceChainId": CFG["chain"], "contractAddress": ca,
                              "requestId": str(uuid.uuid4())}, {"source": "agent"})
    return (r or {}).get("data")

def token_market(ca):
    """One endpoint returns both price and liquidity — two fields per call."""
    d = (http_json(PRICE_URL.format(c=CFG["chain"], a=ca)) or {}).get("data") or {}
    return fnum(d.get("price")), fnum(d.get("liquidity"))

# ---------------- Capital gates ----------------
# RUNNING these checks is the mechanism layer's job and hooks cannot bypass it,
# but the THRESHOLDS AND SWITCHES come from the config. Set a threshold wide, or
# turn an optional block off, and the scaffold complies — this is a suggested
# set of guardrails, not a safety guarantee. How effective they are depends on
# the operator's values.
def native_balance():
    ok, d = baw("wallet", "balance", "--tokenAddress", NATIVE, "--binanceChainId", CFG["chain"])
    if not ok or not isinstance(d, list) or not d: return None
    return fnum(d[0].get("balance"))

def gate_ok(tk):
    """Returns (may we open?, reason)."""
    if os.path.exists(STOP_F): return False, "STOP gate"
    if len(S["pos"]) >= CFG["max_positions"]:
        return False, f"positions full {len(S['pos'])}/{CFG['max_positions']}"
    if S["deployed"] + CFG["position_usd"] > CFG["budget_usd"] + 1e-9:
        return False, f"budget ${S['deployed']:.0f}/{CFG['budget_usd']:.0f}"
    b = native_balance()
    if b is None: return False, "native balance unreadable (fail-closed)"
    if b < CFG["gas_floor_native"]: return False, f"gas floor {b:.6f}<{CFG['gas_floor_native']}"
    ok, d = baw("wallet", "tx-lock", "--binanceChainId", CFG["chain"])
    if ok and (d or {}).get("status") == "LOCKED": return False, "wallet locked (pending tx)"
    ok, d = baw("wallet", "left-quota")
    if ok and fnum((d or {}).get("quotaLeft"), 1e18) < CFG["position_usd"]:
        return False, "daily quota exhausted"
    return True, "ok"

# ---------------- Mechanism-forced check ----------------
# The only thing that cannot be switched off is the act of consulting the audit
# before proceeding. Whether a missing audit rejects the trade (require_audit)
# and whether honeypots are blocked (block_honeypot) are both config decisions.
def hard_gate(ctx):
    """The mechanism-forced check: the audit must have returned a result.
    Whether honeypots are blocked is decided by policy.block_honeypot (default true).
    Every other token-quality judgement lives in the should_enter hook, i.e. with you."""
    a, p = ctx.get("audit"), ctx["policy"]
    if a is None or not a.get("hasResult") or not a.get("isSupported"):
        return (not p.get("require_audit", False)), "audit has no result"
    if p.get("block_honeypot", True) and any(
            d.get("isHit") and "honeypot" in (d.get("title", "") + d.get("description", "")).lower()
            for it in (a.get("riskItems") or []) for d in (it.get("details") or [])):
        return False, "HONEYPOT"
    return True, "ok"

def audit_tax(a):
    """Pull buyTax + sellTax out of an audit response, for use by the hooks."""
    ex = (a or {}).get("extraInfo") or {}
    return (fnum(ex.get("buyTax"), 0.0) or 0) + (fnum(ex.get("sellTax"), 0.0) or 0)

# ---------------- Execution ----------------
# REMOVED 2026-11-19 (Papao): actual_qty() deleted. It polled the order list
# to confirm a live fill; the live fill path no longer exists. Any stale caller
# fails with NameError (intentional).

def qstr(q, dp=8):
    """Quantity formatting: always truncate downward, never round up.

    f"{q:.8f}" rounds — a value one ulp above the balance is enough for the
    platform to answer
      "[01001001] insufficient balance for X, please top up your gas token"
    The message points at gas; the real cause is a single order asking for more
    than the balance. Note the TOTAL committed across orders may exceed the
    balance (a 100% stop-loss and a 50% take-profit coexist happily), so the
    problem is never the total, only an individual order.
    """
    from decimal import Decimal, ROUND_DOWN
    return str(Decimal(str(q)).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_DOWN))

def dec(x, sig=8):
    """Format a price as a plain decimal string.

    f"{x:.12g}" cannot be used — %g switches to scientific notation once the
    exponent drops below -4 (e.g. 7.98e-05), and limit-order's --triggerPrice
    rejects that:
      "Invalid trigger price. Must be a positive number (e.g., $100 or 100)"
    Significant digits are also capped at 8 and decimal places truncated so the
    value is accepted under every chain's precision rules; price triggers do not
    need more.

    Why this matters asymmetrically: a stop-loss trigger is always BELOW the
    entry price, so on a low-priced token the stop-loss is the order that fails
    while the take-profit (a higher number) goes through — leaving a position
    with an upside order and no downside protection, which reads as success in
    the log.
    """
    from decimal import Decimal, ROUND_DOWN
    x = float(x)
    if x == 0: return "0"
    q = Decimal(f"{x:.{sig}e}")                       # fix significant digits first
    s = format(q, "f")                                # plain decimal notation (never %g)
    if "." in s and len(s.split(".")[1]) > MAX_DP:    # then truncate decimal places
        t = format(q.quantize(Decimal(1).scaleb(-MAX_DP), rounding=ROUND_DOWN), "f")
        if Decimal(t) == 0:
            # The price is below 10^-MAX_DP, so truncation would yield 0 and the
            # value cannot be expressed within the precision ceiling. Return None
            # so the caller skips explicitly and warns — never place an order
            # with a trigger price of 0.
            return None
        s = t
    return s.rstrip("0").rstrip(".") if "." in s else s

# REMOVED 2026-11-19 (Papao): proceeds_from_tx() deleted with the live exit
# flow. It read on-chain exit proceeds for positions that can no longer exist.
# Any stale caller fails with NameError (intentional).

# REMOVED 2026-11-19 (Papao): place_protection() deleted. It placed on-chain
# limit orders (stop-loss / take-profit) via the wallet CLI. The live execution
# path no longer exists. Any stale caller fails with NameError (intentional).

def open_position(ev, ctx, lat):
    ca, tk = ev["ca"], ev["token"] or "?"
    px = ctx["price"]
    usd = min(fnum(size_position(ev, ctx), 0.0) or 0.0,
              CFG["position_usd"],
              CFG["budget_usd"] - S["deployed"])          # mechanism-layer clamp
    if usd <= 0: return dict(decision="size=0")
    # LIVE TRADING REMOVED 2026-11-19 (Papao): the live branch that used to
    # follow here (swap, fill confirmation, balance fallback, protection
    # placement, position recording) was deleted. This function always returns
    # DRY_RUN; no order is ever placed.
    return dict(decision="DRY_RUN", entry=px, would_spend=round(usd, 2))

# ---------------- Outcome sampling ----------------
# events.jsonl answers "what did the strategy decide". On its own it cannot
# answer "was the decision any good", which is the question that matters when
# you are deciding whether to risk money. So every decision that would have
# opened a position schedules a few price re-reads, and the results land in
# outcomes.jsonl keyed by the same event key.
#
# This runs in dry-run too — that is the point. It lets a strategy be scored
# from recorded data instead of from real fills, which is the only way to get a
# usable sample size without funding the experiment.
#
# Caveats worth knowing before you trust the numbers:
#   · These are marks, not fills. No slippage, no fees, no tax, no gas, and no
#     check that the position could actually have been exited at that price.
#     Treat them as an upper bound on what the strategy could have captured.
#   · A horizon only tells you the price at that instant. It does not tell you
#     whether a stop-loss would have been touched first — for that you need the
#     path, so use several horizons and read them together.
#   · Pending samples are persisted in state.json, so a restart does not lose
#     them, but a long outage means some are read late. `sampled_late` marks
#     those rather than silently distorting the series.

def schedule_followups(ev, entry):
    """Queue price re-reads for one decision. Called from the worker threads, so
    every mutation of S["followups"] is under FOLLOWUP_LK — see followup_worker
    for why replacing that list without a lock loses entries."""
    hs = CFG.get("outcome_horizons_min") or []
    if not hs or not entry or entry <= 0: return
    nowms = int(time.time() * 1000)
    new = [dict(key=ev["key"], ca=ev["ca"], token=ev["token"], src=ev["src"],
                t0_ms=nowms, entry=entry, horizon_min=h,
                due_ms=nowms + int(h * 60_000)) for h in hs]
    dropped = 0
    cap = 5000
    with FOLLOWUP_LK:
        pend = S.setdefault("followups", [])
        pend.extend(new)
        # Bound the queue. Overflow means the sampler cannot keep up (or the
        # horizons are far too long); dropping the oldest beats growing without
        # limit, and it is logged rather than hidden.
        if len(pend) > cap:
            dropped = len(pend) - cap
            del pend[:dropped]
    if dropped:
        log(f"  !! outcome queue over {cap}, dropped {dropped} oldest pending sample(s)")
    save()

def followup_worker():
    """Sample due follow-ups and append to outcomes.jsonl."""
    if not (CFG.get("outcome_horizons_min") or []): return
    while not os.path.exists(KILL_F):
        time.sleep(20)
        try:
            # Snapshot under the lock, do the slow work outside it, then remove
            # exactly what was sampled — again under the lock. Replacing the
            # whole list instead would silently lose anything a worker thread
            # appended while the market-data calls were in flight, and that
            # window is seconds wide.
            with FOLLOWUP_LK:
                pend = list(S.get("followups") or [])
            if not pend: continue
            nowms = int(time.time() * 1000)
            due = [x for x in pend if x.get("due_ms", 0) <= nowms]
            if not due: continue
            # One market-data call per distinct contract, not per sample.
            prices = {}
            for ca in {x["ca"] for x in due}:
                px, _liq = token_market(ca)
                prices[ca] = px
            for x in due:
                px = prices.get(x["ca"])
                ret = ((px / x["entry"] - 1) * 100) if (px and x.get("entry")) else None
                late_s = round((nowms - x["due_ms"]) / 1000)
                jsonl(OUTJ, dict(key=x["key"], ca=x["ca"], token=x.get("token"),
                                 src=x.get("src"), horizon_min=x["horizon_min"],
                                 t0_ms=x["t0_ms"], entry=x["entry"],
                                 price=px, ret_pct=(round(ret, 4) if ret is not None else None),
                                 sampled_ms=nowms,
                                 sampled_late=(late_s if late_s > 120 else None)))
            sampled = {(x["key"], x["horizon_min"]) for x in due}
            with FOLLOWUP_LK:
                cur = S.get("followups") or []
                S["followups"] = [x for x in cur
                                  if (x.get("key"), x.get("horizon_min")) not in sampled]
            save()
        except Exception as e:
            log("  [outcome] ERR", repr(e))

# ---------------- Event normalization ----------------
def norm_address(e):
    """Address stream: one on-chain trade by a followed wallet."""
    return dict(src="address", key=str(e.get("txHash")),
        ca=(e.get("ca") or ""), token=e.get("tokenName"),
        price=fnum(e.get("tokenPrice")), ts=e.get("ts"),
        chain=str(e.get("chainId")), side=e.get("tradeSideCategory"),
        who=e.get("label") or e.get("address"), usd=fnum(e.get("txUsdValue")),
        risk=e.get("tokenRiskLevel"), top10=fnum(e.get("top10HoldersPercentage")),
        tags=[t["tagName"] for g in (e.get("tokenTag") or {}).values() for t in g],
        extra=dict(addr=e.get("address")))

def norm_signal(e):
    """Signal stream: a smart-money signal decided by the platform."""
    tt = e.get("signalTriggerTime")
    return dict(src="signal", key="sig:" + str(e.get("signalId")),
        ca=(e.get("contractAddress") or ""), token=e.get("ticker"),
        price=fnum(e.get("currentPrice")) or fnum(e.get("alertPrice")),
        ts=(tt / 1000 if tt else None),
        chain=str(e.get("chainId")), side=11,      # a signal is a buy intent
        who=f"SMY×{e.get('smartMoneyCount')}", usd=fnum(e.get("totalTokenValue")),
        risk=None, top10=fnum(e.get("top10")),
        tags=[t["tagName"] for g in (e.get("tokenTag") or {}).values() for t in g],
        # `extra` is splatted wholesale into events.jsonl, so every field that is
        # available at decision time is captured for later "feature vs outcome"
        # analysis. Fields present on the first push: alertLiquidity,
        # entryLiquidity, top10, holders, smartMoneyCount, isAlpha, launchTime.
        # status / exitRate / currentPrice are usually null there — do not rely
        # on them for entry decisions.
        extra=dict(signalId=e.get("signalId"), status=e.get("status"),
                   smy=e.get("smartMoneyCount"), exitRate=e.get("exitRate"),
                   liq=fnum(e.get("alertLiquidity")),
                   entry_liq=fnum(e.get("entryLiquidity")),
                   holders=fnum(e.get("holders")), is_alpha=e.get("isAlpha"),
                   launch_ms=e.get("launchTime"), mcap=fnum(e.get("alertMarketCap")),
                   sig_seq=e.get("sequence")))

# ---------------- Event handling ----------------
def handle(ev, arrived, conn):
    lat = {}
    row = dict(arrived_ms=int(arrived*1000), src=ev["src"], key=ev["key"], ts=ev["ts"],
               lag_s=(round(arrived-ev["ts"], 2) if ev["ts"] else None),
               conn_uptime_s=round(arrived-conn["at"], 1) if conn.get("at") else None,
               conn_seq=conn.get("seq"), token=ev["token"], ca=ev["ca"], chain=ev["chain"],
               side=ev["side"], who=ev["who"], usd=ev["usd"], riskLevel=ev["risk"],
               sig_price=ev["price"],          # log the signal price for EVERY event, rejected
                                               # ones included — otherwise there is no way to
                                               # check afterwards whether a rejection was right
               top10=ev["top10"], tags=ev["tags"], **{k: v for k, v in ev["extra"].items()})
    if ev["ts"] and conn.get("at") and ev["ts"] < conn["at"]: row["replay"] = True
    def emit(dec=None, **kw):
        if dec is not None: kw["decision"] = dec
        row.update(latency_ms=lat, **kw); jsonl(EVJ, row)
        with OPENING_LK: OPENING.discard(ev["ca"].lower())

    LAST_PUSH[0] = arrived; PUSHES[0] += 1      # count every push, re-pushes included
    if ev["key"] in S["handled"]: return
    S["handled"].append(ev["key"]); S["handled"] = S["handled"][-4000:]
    S["last_event_ms"] = int(arrived*1000); save()
    if not ev["ca"]: emit("no ca"); return
    if ev["chain"] != str(CFG["chain"]): emit(f"chain={ev['chain']}"); return

    policy = CFG.get("policy") or {}
    tag = f"[{ev['src'][:3]}] {str(ev['who'])[:12]:<12} {str(ev['token'])[:10]:<10}"

    # 1) Ask the strategy hook first — no point paying for an audit on something
    #    that will be rejected anyway.
    ctx = dict(audit=None, liquidity=None, enriched=False, price=ev["price"], positions=S["pos"],
               deployed=S["deployed"], cfg=CFG, policy=policy)
    ok, why = should_enter(ev, ctx)
    if not ok: emit(why); return

    # 2) Mechanism guardrails.
    # Same-token dedupe needs a lock plus a reservation: two signals for the same
    # token can arrive a second apart and both pass this check before either is
    # written into S["pos"], doubling the position on that token.
    # OPENING doubles as the in-flight reservation ledger — budget and position
    # count must include in-flight opens, otherwise several workers read the same
    # `deployed` value, each concludes there is room, and the budget and position
    # ceilings are both exceeded.
    with OPENING_LK:
        cal = ev["ca"].lower()
        if cal in OPENING or any(p["ca"].lower() == cal for p in S["pos"].values()):
            emit("already holding this token"); return
        # Same-token cooldown: buy only the earliest signal within the window.
        # "Do I hold it right now" is not enough — once a position closes, later
        # signals for the same token would pass again (one token can produce
        # several distinct signals in a day).
        cd_h = (ctx["policy"] or {}).get("same_token_cooldown_h", 24)
        if cd_h:
            last = (S.get("ca_last") or {}).get(cal)
            if last and (time.time()*1000 - last) < cd_h * 3600_000:
                hrs = (time.time()*1000 - last) / 3600_000
                emit(f"same-token cooldown {hrs:.1f}h/{cd_h}h"); return
        inflight = len(OPENING)
        need = CFG["position_usd"]
        # Profitable-exit bonus allowance: each exit that settles at a profit adds
        # one position_usd slot. Losing exits add nothing, and neither do exits
        # whose proceeds cannot be determined (proceeds=None) — fail-closed.
        bonus = int(S.get("bonus_slots") or 0)
        cap_pos = CFG["max_positions"] + bonus
        cap_usd = CFG["budget_usd"] + bonus * need
        if len(S["pos"]) + inflight >= cap_pos:
            emit(f"positions full {len(S['pos'])}+{inflight}/{cap_pos}"
                 f" (base {CFG['max_positions']} + bonus {bonus})"); return
        if S["deployed"] + inflight * need + need > cap_usd + 1e-9:
            emit(f"budget exhausted: deployed ${S['deployed']:.0f} + in-flight {inflight}×${need:.0f}"
                 f" / ${cap_usd:.0f} (base ${CFG['budget_usd']:.0f} + bonus {bonus}×${need:.0f})"); return
        OPENING.add(cal)
    ok, why = gate_ok(tag)
    if not ok: log(f"  {tag} ⏸ {why}"); emit(why); return

    # 3) Complete ctx, then let the hook judge a second time.
    #    Whether audit and market data are fetched depends on the source
    #    (policy.enrich_srcs, address stream only by default):
    #      · address stream: tokens are often newly launched, the event carries
    #        no liquidity, and the audit is the only risk signal → must fetch
    #      · signal stream: alertLiquidity / alertPrice are on the first push and
    #        market data is redundant; skipping both saves a network round trip
    #        (the two requests run concurrently, so the cost is the slower one)
    enrich = ev["src"] in ((ctx["policy"] or {}).get("enrich_srcs") or ["address"])
    a = api_px = liq = None
    if enrich:
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=2) as ex:
            fa, fm = ex.submit(audit, ev["ca"]), ex.submit(token_market, ev["ca"])
            a = fa.result(); api_px, liq = fm.result()
        lat["audit_market_ms"] = int((time.time()-t0)*1000)
    else:
        lat["audit_market_ms"] = 0
    px, psrc = ev["price"], "event"
    if not px: px, psrc = api_px, "api"
    ctx.update(audit=a, liquidity=liq if liq is not None else ev["extra"].get("liq"),
               price=px, enriched=True)
    row.update(px_src=psrc, liquidity=ctx["liquidity"],
               tax=audit_tax(a), audit_risk=(a or {}).get("riskLevel"))

    ok, why = hard_gate(ctx)
    if not ok: log(f"  {tag} ⛔ {why}"); emit("hard_gate:"+why); return
    if not px: emit("no price"); return
    ok, why = should_enter(ev, ctx)          # second call: now with audit and liquidity
    if not ok: log(f"  {tag} ✗ {why}"); emit(why); return

    log(f"  {tag} ✅ lag={row['lag_s']}s tax={row['tax']:.2%} liq={ctx['liquidity']}")
    res = open_position(ev, ctx, lat)
    emit(**res)
    # Score this decision later, whether or not real money was involved.
    if res.get("decision") in ("DRY_RUN", "OPENED"):
        schedule_followups(ev, fnum(res.get("entry")) or fnum(ctx.get("price")))

# ---------------- Reconciliation ----------------
def reconcile():
    """Liveness metrics only.

    REMOVED 2026-11-19 (Papao): the protective-order reconciliation (order
    list reads, cancels, re-placing protection, closed-position ledger) was
    deleted with all live-trading code. In dry-run mode no position is ever
    opened, so there is nothing to reconcile.
    """
    while True:
        if LAST_PUSH[0]:
            S["last_push_ms"] = int(LAST_PUSH[0]*1000); S["pushes"] = PUSHES[0]; save()
        time.sleep(CFG["reconcile_sec"])

# ---------------- Main loop ----------------
def acquire_lock():
    """Single-instance lock, held with flock for the life of the process.

    A duplicate start means two WS streams, double orders, and two processes
    overwriting each other's state.json — under live mode that is literally
    double position sizing, so this has to be airtight.

    Why flock rather than a pidfile check:
      · `os.path.exists()` followed by a write is a TOCTOU window — two
        processes starting together both see no file and both proceed.
      · O_CREAT|O_EXCL closes that window for creation, but "create the file"
        and "write the pid into it" are still two steps, so a second process can
        read a momentarily empty file, judge it corrupt, delete it, and take the
        lock. (Observed while testing the O_EXCL version: 12 concurrent
        attempts, 3 winners.)
      · flock is a single kernel-arbitrated operation with no such window, and
        the kernel releases it when the holder dies — which removes the whole
        notion of a stale lock that has to be detected and cleaned up.

    The pid is still written into the file, purely so a human can see who holds
    it. Exclusivity does not depend on that content.

    POSIX only (Linux/macOS), consistent with the rest of this script.
    """
    import fcntl
    global _LOCK_FD
    try:
        fd = os.open(LOCK_F, os.O_CREAT | os.O_RDWR, 0o644)
    except OSError as e:
        log(f"!! could not open {LOCK_F}: {e}")
        return False
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (BlockingIOError, OSError):
        try:
            holder = os.read(fd, 32).decode(errors="replace").strip() or "unknown"
        except Exception:
            holder = "unknown"
        os.close(fd)
        log(f"!! another instance holds {LOCK_F} (pid {holder}) — not starting a second one")
        return False
    # Lock held. Record the pid for human diagnosis only.
    try:
        os.ftruncate(fd, 0)
        os.write(fd, str(os.getpid()).encode())
        os.fsync(fd)
    except OSError:
        pass
    _LOCK_FD = fd          # keep the descriptor open; closing it releases the lock
    import atexit
    def _release():
        try: os.remove(LOCK_F)
        except OSError: pass
        try: os.close(fd)
        except OSError: pass
    atexit.register(_release)
    return True

def ws_reader(src, argv, q, conns):
    """One WS child process per source. The reader thread only timestamps and
    enqueues; it never makes a blocking call.

    ── Connection-level care belongs to the CLI; this function only supervises
       the process ──
    `tracker ws --duration 0` has application-level PING keepalive, automatic
    reconnect with re-SUBSCRIBE on close, and bounded exponential backoff (reset
    on any received push) built in. Parameters are documented in the
    "Connection lifecycle" section of `binance-wallet-tracker`, which also
    explicitly asks callers not to add a second connection-level layer, because:
      · an outer "active rotation" kills a connection the CLI was maintaining fine
      · an outer watchdog force-kills the child while the CLI is mid-backoff,
        aborting a pending reconnect
    So all that remains here is "restart the child only if it actually exited",
    on a fixed short delay — no backoff, no rotation, no silence watchdog. Long
    stretches without a new push during a quiet market are normal, not a fault.

    The required CLI version is the `requiredCliVersion` in SKILL.md's
    frontmatter (mirrored by CLI_MIN below). Below that version `--duration 0`
    has neither keepalive nor reconnect and a caller must implement its own —
    the startup check refuses to run in that case.
    """
    conn = conns[src] = {"at": None, "seq": 0}
    norm = norm_address if src == "address" else norm_signal
    restarts = 0
    while not os.path.exists(KILL_F):
        p = subprocess.Popen(["baw", "tracker", "ws", *argv, "--duration", "0"],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True, bufsize=1)
        conn["at"] = time.time(); conn["seq"] += 1
        rows = 0
        try:
            for line in p.stdout:
                line = line.strip()
                if not line.startswith("{"): continue
                arrived = time.time(); rows += 1
                try: e = json.loads(line)
                except Exception: continue
                try: n = norm(e)
                except Exception: continue
                if not n.get("key") or n["key"] in ("None", "sig:None"): continue
                q.put((n, arrived, dict(conn)))
                if q.qsize() > 80: log(f"  !! backlog {q.qsize()} events")
                if os.path.exists(KILL_F): break
        except Exception as ex:
            log(f"[{src}] read error {ex!r}")
        finally:
            try: p.kill()
            except Exception: pass
        if os.path.exists(KILL_F): return

        # A child exit means the CLI's own reconnect gave up too. That is a
        # process-level fault and deserves an alarm.
        restarts += 1
        S["stream_alarm"] = dict(t=now(), src=src, restarts=restarts,
                                 rows_last_run=rows, seq=conn["seq"])
        save()
        log(f"[{src}] child exited (received {rows} events this run), restart #{restarts}. "
            f"The CLI's built-in reconnect gave up — check session and network")
        time.sleep(PROC_RESTART_SEC)

def health(conns, q):
    while True:
        time.sleep(3600)
        try:
            c = " | ".join(f"{k}: connection #{v['seq']}, stable for {(time.time()-v['at'])/60:.0f}min"
                           for k, v in conns.items() if v.get("at"))
            f = f" | ⚠️ {FAILS[0]} order failure(s)" if FAILS[0] else ""
            log(f"[health] {c} | pushes {PUSHES[0]} | queue {q.qsize()} | positions {len(S['pos'])}"
                f" | deployed ${S['deployed']:.2f}{f}")
        except Exception: pass

CLI_MIN = (1, 9, 1)   # built-in keepalive/reconnect for --duration 0 starts at this version

def cli_version_ok():
    """Below the required version `--duration 0` has no keepalive and no
    reconnect, while this script no longer carries connection-level reconnect of
    its own — running anyway goes permanently silent after the first disconnect.
    That has to be blocked at startup. The required version is CLI_MIN.

    Mind what `cli-check` returns: `success` only reports that the command ran
    and is **always true**; the actual verdict is in `data.needUpdateCli`.
    Treating `success` as "version is fine" makes this gate useless.
        {"success": true, "data": {"currentCliVersion": "x.y.z", "needUpdateCli": true}}
    """
    ok, d = baw("cli-check", "--required-version", ".".join(map(str, CLI_MIN)))
    cur = (d or {}).get("currentCliVersion") if isinstance(d, dict) else None
    if not ok:
        return False, cur or "query failed"
    if (d or {}).get("needUpdateCli"):
        return False, cur or "unknown"
    return True, cur

# REMOVED 2026-11-19 (Papao): live_confirmed() deleted in full, together
# with the acknowledgement-file mechanism. Live trading is technically
# impossible in this script; the startup guard above refuses any mode value
# other than "dry-run".

def main():
    if not acquire_lock(): return
    missing = check_cfg(CFG)
    if missing:
        log(f"!!! configuration incomplete, refusing to start ({len(missing)} field(s)):")
        for k in missing: log(f"      {k}")
        log(f"    These parameters have no defaults — fill each one in {CFG_F}.")
        log("    Their meaning and how to choose them are in SKILL.md; if unsure, "
            "run dry-run for a while first.")
        return
    ok, cur = cli_version_ok()
    if not ok:
        log(f"!!! CLI version too low: need >= {'.'.join(map(str, CLI_MIN))}, found {cur}")
        log("    Below that version `tracker ws --duration 0` has no keepalive and no reconnect, "
            "while this script has removed connection-level reconnect to match the newer "
            "semantics — it would go permanently silent after a disconnect. Upgrade the CLI first.")
        return
    FAILS[0] = int(S.get("buy_fails") or 0)      # cumulative across restarts
    ok, qb = baw("wallet", "balance", "--tokenAddress", CFG["quote_token"],
                 "--binanceChainId", CFG["chain"])
    if ok and isinstance(qb, list) and qb:
        QUOTE_MARK[0] = fnum(qb[0].get("balance"), 0.0)
        log(f"quote-token balance baseline {QUOTE_MARK[0]:.6f}")
    log("=" * 72)
    log(f"COPY TRADER start #{S.get('runs',0)+1} | mode={CFG['mode'].upper()} "
        f"(dry-run only — no real orders)")
    log(f"chain={CFG['chain']} sources={CFG['sources']} quote={CFG['quote_token'][:10]}…")
    log(f"budget=${CFG['budget_usd']} per-trade=${CFG['position_usd']} "
        f"max positions={CFG['max_positions']} gas floor={CFG['gas_floor_native']}")
    log(f"policy={json.dumps(CFG.get('policy') or {}, ensure_ascii=False)}")
    hs = CFG.get("outcome_horizons_min") or []
    log(f"outcome sampling: {hs} min → outcomes.jsonl" if hs else "outcome sampling: off")
    al = os.path.join(D, CFG["address_list"])
    srcs = {}
    if "address" in CFG["sources"]:
        if not os.path.exists(al):
            with open(al, "w") as f:
                f.write("# One address per line, max 100. Lines starting with # are comments.\n"
                        "# See SKILL.md \"Source selection\" for how to build this list, e.g.\n"
                        "#   baw leaderboard query -c <chain> -p 7d --sort-by 20 --size 20 --page 0 --json\n")
            log(f"!! wrote an empty address list {al} — fill it in and restart. "
                f"See SKILL.md \"Source selection\""); return
        n = sum(1 for l in open(al) if l.strip() and not l.startswith("#"))
        log(f"address stream: {n} address(es)"
            + ("  !! exceeds the --address-list cap of 100" if n > 100 else ""))
        srcs["address"] = ["--address-list", al, "-c", CFG["chain"]]
    if "signal" in CFG["sources"]:
        log("signal stream: --smy (all-chain push, filtered by chain)")
        srcs["signal"] = ["--smy"]
    if not srcs: log("!! `sources` is empty, exiting"); return

    S["runs"] = S.get("runs", 0) + 1; save()
    q = queue.Queue(); conns = {}
    def worker():
        while True:
            item = q.get()
            if item is None: return
            n, arr, conn = item
            try: handle(n, arr, conn)
            except Exception as ex:
                import traceback
                log("  handle ERR", repr(ex), "|", traceback.format_exc().strip().splitlines()[-2].strip())
            finally:
                # If handle raises after the reservation is taken, emit never
                # runs, so the reservation must be released here — otherwise that
                # contract address is blocked forever (fail-safe, but it would
                # silently drop every later opportunity on that token).
                try:
                    with OPENING_LK: OPENING.discard((n.get("ca") or "").lower())
                except Exception: pass
                q.task_done()
    for _ in range(CFG.get("workers", 4)): threading.Thread(target=worker, daemon=True).start()
    threading.Thread(target=reconcile, daemon=True).start()
    threading.Thread(target=followup_worker, daemon=True).start()
    threading.Thread(target=health, args=(conns, q), daemon=True).start()
    for src, argv in srcs.items():
        threading.Thread(target=ws_reader, args=(src, argv, q, conns), daemon=True).start()

    while not os.path.exists(KILL_F): time.sleep(5)
    log("KILL — exiting (on-chain orders remain active)")

if __name__ == "__main__":
    main()
