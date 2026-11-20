# Custom Signal — `baw signal` CLI Reference

Complete reference for all `baw signal` subcommands.

**Invocation pattern**: `baw signal <subcommand> [options] --json`
**Exit codes**: `0` success · `1` usage/upstream error · `3` network failure
**JSON mode**: Always pass `--json` for structured output. The CLI wraps responses as `{ success, data, error }`.

---

## `baw signal list` — Signal Feed

Multi-source signal feed. By default fetches all three sources concurrently and merges.

```bash
baw signal list -c 56 --json
baw signal list -c 56 --source user --sort-by maxGain --time-range 24h --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | no | `56` | Chain ID (`56` BSC, `CT_501` Solana) |
| `-n, --page-size` | number | no | `100` | Items per source. **Max 100** — values >100 return `INVALID_PARAMS` (1001002). |
| `-s, --source` | enum | no | `all` | `all` / `user` / `meme` / `smart-money` |
| `--strategy-id` | string | no | — | Filter by strategy ID (USER_STRATEGY only). When specified with `--source all`, CLI auto-switches to `user` source. |
| `--strategy-type` | enum | no | — | `meme-rush` / `fomo-call` (USER_STRATEGY only; aliases: `meme`, `fomo`). Filtered client-side since the API ignores this parameter. |
| `--sort-by` | enum | no | `time` | `time` / `maxGain` |
| `--time-range` | enum | no | — | `5m` / `1h` / `24h` |

### JSON Output Structure

**When `--source all`** (default), output is a wrapper object with partial failure info:

```json
{
  "success": true,
  "data": {
    "list": [ /* SignalItem[] */ ],
    "allSucceeded": true,
    "failedSources": []
  }
}
```

**When `--source user|meme|smart-money`** (specific source), output is a flat array:

```json
{
  "success": true,
  "data": [ /* SignalItem[] */ ]
}
```

### SignalItem Fields

| Field | Type | SMART_MONEY | USER/MEME | Description |
|-------|------|:-----------:|:---------:|-------------|
| `signalId` | number | ✅ | ✅ | Unique signal ID |
| `ticker` | string | ✅ | ✅ | Token ticker |
| `signalSource` | string | ✅ | ✅ | `SMART_MONEY` / `USER_STRATEGY` / `MEME_OFFICIAL` |
| `strategyType` | string | — | ✅ | `meme-rush` / `fomo-call` |
| `direction` | string | ✅ | — | `buy` / `sell` |
| `alertPrice` | string | ✅ | ✅ | Trigger price |
| `alertMarketCap` | string | ✅ | ✅ | Trigger market cap |
| `currentPrice` | string | ✅ | — | Current price (SMART_MONEY only) |
| `currentMarketCap` | string | ✅ | — | Current market cap (SMART_MONEY only) |
| `highestPrice` | string | ✅ | ✅ | Highest price since trigger |
| `highestPriceTime` | number | ✅ | ✅ | Timestamp of peak (ms) |
| `maxGain` | string | ✅ | ✅ | Decimal fraction (0.25 = 25%) |
| `peakArrivalCostMs` | number | — | ✅ | Time from trigger to peak (ms) |
| `smartMoneyCount` | number | ✅ | — | Smart money count |
| `smartSignalType` | string | ✅ | — | `SMART_KOL` etc |
|| `exitRate` | number | ✅ | ✅ | Exit rate (0-100 integer; primarily meaningful for SMART_MONEY; ≥ 70 = may have passed) |
| `goldenRate` | number | — | ✅ | Golden dog rate (0-1) |
| `silverDogRate` | number | — | ✅ | Silver dog rate (0-1) |
| `bronzeDogRate` | number | — | ✅ | Bronze dog rate (0-1) |
| `winRate` | number | — | ✅ | Win rate (0-1) |
|| `status` | string | ✅ | ✅ | Signal status: `valid` (fresh), `timeout` (stale), `outDecline` (price declining), `exitRate` (exit threshold reached), or `null` |
| `jobId` | string | — | ✅ | Job ID for strategy operations |
| `strategyId` | string | — | ✅ | Strategy ID |
| `strategyName` | string | — | ✅ | Strategy name |
| `signalTriggerTime` | number | ✅ | ✅ | Trigger timestamp (ms) |
| `tokenTag` | object | ✅ | ✅ | Categorized tags (e.g. `{"Launch Platform": [{"tagName": "Pumpfun"}]}`) |
| `isAlpha` | boolean | ✅ | ✅ | Alpha token flag |
| `alphaPoint` | number | ✅ | ✅ | Alpha points |
| `launchPlatform` | string | ✅ | ✅ | Launch platform name |
| `isExclusiveLaunchpad` | boolean | ✅ | ✅ | Exclusive launchpad flag |
| `latestBacktestTime` | number | — | ✅ | Last backtest run timestamp (ms) |

### Partial Failure

When `--source all`, some sources may fail while others succeed:

```json
{
  "success": true,
  "data": {
    "allSucceeded": false,
    "failedSources": [{ "source": "smart-money", "error": "Network timeout" }],
    "list": [/* partial results */]
  }
}
```

If all sources fail: `success: false`. Treat as an error, not "no signals".

---

## Strategy Management Commands — REMOVED by this modification (Papao, 2026-11-19)

`baw signal strategy create/update/delete/follow/unfollow` documentation was removed. This skill is read-only.

## `baw signal strategy list` — List Owned Strategies

```bash
# List all owned strategies (both meme-rush and fomo-call)
baw signal strategy list -c 56 --json

# Only show enabled (followed) strategies
baw signal strategy list -c 56 --followed --json

# Filter by strategy type
baw signal strategy list -c 56 --type fomo-call --json
baw signal strategy list -c 56 --type meme-rush --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | Chain ID |
| `--followed` | flag | no | — | Only show enabled strategies |
| `--type` | enum | no | — | Filter by strategy type: `meme-rush` \| `fomo-call` (aliases: `meme`, `fomo`). When omitted, both types are queried and merged. |

> **Auto-pagination**: This command auto-paginates internally — no `-p`/`-s` parameters needed. It fetches all owned strategies across all pages. When `--type` is omitted, the CLI queries both `meme-rush` and `fomo-call` types concurrently and merges the results.

### JSON Output

```json
{
  "success": true,
  "data": [
    {
      "strategy_id": "string",
      "strategy_name": "string",
      "strategy_type": "meme-rush",
      "job_id": "string",
      "task_id": "string",
      "followed": true
    }
  ]
}
```

> **Note on `strategy_type`**: Due to backend pagination behavior, some entries may have `strategy_type` as null or empty string. When processing the list, deduplicate by `job_id` + `task_id` and fill missing `strategy_type` by inferring from `job_id` prefix (`fomo-call-*` → `fomo-call`, `meme-rush-*` → `meme-rush`). Never expose null/empty `strategy_type` to the user — always display a valid type per the Term Mapping rules.

---

## `baw signal strategy list-followed` — List Followed Strategies

```bash
baw signal strategy list-followed -c 56 --json
```

### JSON Output

```json
{
  "success": true,
  "data": [
    { "strategy_id": "string", "strategy_name": "string", "strategy_type": "string", "job_id": "string" }
  ]
}
```

---

## `baw signal backtest list` — List Backtests

```bash
# Single page (shows pagination info in terminal mode)
baw signal backtest list -c 56 --json
baw signal backtest list -c 56 -p 2 -s 50 --backtest-days 30 --json

# Auto-paginate — fetch all pages, return complete list
baw signal backtest list -c 56 --all --json
baw signal backtest list -c 56 --all --backtest-days 30 --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | Chain ID |
| `-p, --page` | number | no | `1` | Page number (ignored when `--all` is used) |
| `-s, --size` | number | no | `20` | Page size (backend may cap to 10) |
| `--backtest-days` | number | no | — | Backtest period in days |
| `--all` | flag | no | — | Auto-paginate to fetch all pages. Overrides `--page`/`--size`. |

### JSON Output

**Without `--all`** (single page) — returns `TaskStatsPage` with pagination metadata:

```json
{
  "success": true,
  "data": {
    "taskList": [ /* TaskStats[] */ ],
    "page": 1,
    "size": 10,
    "total": 7,
    "totalPages": 1
  }
}
```

**With `--all`** — returns the complete list with total count:

```json
{
  "success": true,
  "data": {
    "total": 7,
    "taskList": [ /* TaskStats[] — all pages merged */ ]
  }
}
```

> **Pagination note**: The backend caps `size` to 10 regardless of the requested page size. When you need the full list (e.g. counting strategies, checking `copyTradeStatus` across all jobs), always use `--all` — without it, only the first page is returned.

| Field | Type | Description |
|-------|------|-------------|
| `jobId` | string | Job ID (use for follow/update/delete/retry) |
| `strategyId` | string | Strategy ID (use for detail/unfollow) |
| `taskName` | string | Strategy name |
| `strategyType` | string | `meme-rush` or `fomo-call` |
| `status` | string | `PENDING` / `RUNNING` / `COMPLETED` / `FAILED` / `CANCELLED` |
| `winRate` | number | Win rate (0-1) |
| `signalCount` | number | Total signals generated |
| `tokenCount` | number | Distinct tokens in signals |
| `goldenRate` | number | Golden dog rate (0-1) |
| `silverDogRate` | number | Silver dog rate (0-1) |
| `bronzeDogRate` | number | Bronze dog rate (0-1) |
| `snipePct` | number | Snipe time-to-peak pct (< 1min, 0-1) |
| `quickFlipPct` | number | Quick Flip pct (1–5min, 0-1) |
| `swingPct` | number | Swing pct (5–60min, 0-1) |
| `holdPct` | number | Hold pct (1–24h, 0-1) |
| `moonPct` | number | Moon pct (> 24h, 0-1) |
| `peakArrivalCostP50Ms` | number | Median time-to-peak (ms) |
| `signalTokenFrequency` | number | Signal frequency (signals/day) |
| `scheduleInterval` | string \| null | Schedule interval or null/OFF |
| `lastRunTime` | number \| null | Last backtest run timestamp (ms) |
| `nextRunTime` | number \| null | Next scheduled run timestamp (ms) |
| `followed` | boolean | Whether current user follows this strategy |
| `isOwner` | boolean | Whether current user owns this strategy |
| `copyTradeStatus` | string \| null | Copy trading status (`ACTIVE` = has active copy trading) |
| `copyTradeStrategyId` | string \| null | Copy trade strategy ID |
| `dailySignalLimit` | number | Daily signal trigger limit |
| `todaySignalCount` | number | Today's signal count |
| `limitReached` | boolean | Whether daily limit reached |
| `needRetest` | boolean | Whether retest is recommended |
| `needRetestReason` | string \| null | Reason for retest recommendation |
| `walletGroupName` | string \| null | Wallet group name (fomo-call) |
| `walletAddressCount` | number \| null | Wallet address count (fomo-call) |
| `triggerMinWallets` | number \| null | Min wallets trigger (fomo-call) |
| `triggerMinBuyAmountUSD` | number \| null | Min buy amount per wallet (fomo-call) |
| `triggerTimeWindowMinutes` | number \| null | Time window in minutes (fomo-call) |
| `tokenDetails` | array | Token list with per-token metrics (same as `tokens` in detail) |
| `tokens` | array | Alias for `tokenDetails` (same data, both fields present) |
| `createdAt` | string | Creation datetime (e.g. `"2026-06-30 12:33:44"`) |
| `createdAtTimestamp` | number | Creation timestamp (ms) |
| `updatedAt` | string | Last update datetime |
| `updatedAtTimestamp` | number | Last update timestamp (ms) |
| `lastSignalTokenTime` | number \| null | Last signal token timestamp (ms) |

**Null safety**: Some fields may be `null` (e.g. `winRate`, `scheduleInterval`) for newly created or pending strategies. Always null-check before arithmetic.

---

## `baw signal backtest detail` — Backtest Detail

```bash
baw signal backtest detail -c 56 --strategy-id <strategyId> --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |
| `--strategy-id` | string | yes | Strategy ID |

### JSON Output

```json
{
  "success": true,
  "data": {
    "info": { /* same fields as backtest list item */ },
    "tokens": [
      {
        "chainId": "string",
        "contractAddress": "string",
        "tokenName": "string",
        "symbol": "string",
        "imageUrl": "string",
        "tokenIcon": "string",
        "alertPrice": "number (float)",
        "alertTime": "string (formatted datetime, e.g. \"2026/06/04 12:02:42\")",
        "alertTimestamp": "number (ms)",
        "alertMc": "number (float)",
        "athPrice": "number (float)",
        "athTime": "string (formatted datetime)",
        "athTimestamp": "number (ms)",
        "athMc": "number (float)",
        "incrPercent": "number (decimal fraction, e.g. 26.12 = 2612%)",
        "peakArrivalCostMs": "number (ms)"
      }
    ]
  }
}
```

API: `/backtest/get-task-vo`, param `{ chainId, strategyId }`.

---

## `baw signal backtest retry` / `schedule` — REMOVED by this modification (Papao, 2026-11-19)

Backtest retry and schedule are disabled. List/detail only.

## `baw signal explore` — Explore Official Strategies

```bash
baw signal explore -c 56 --json
baw signal explore -c 56 --backtest-days 30 --json
```

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `-c, --chain-id` | string | yes | — | Chain ID |
| `--backtest-days` | number | no | — | Backtest period in days |

Returns a flat `TaskStats[]` array (not `TaskStatsPage`). Explore returns a **subset** of TaskStats — it has NO user-specific fields (`followed`, `isOwner`, `scheduleInterval`, `dailySignalLimit`, `todaySignalCount`, `limitReached`, `copyTradeStatus`, `copyTradeStrategyId`) but adds official strategy fields:

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Strategy type (may differ from `strategyType` — explore uses `type` field) |
| `signalNameCn` | string | Official strategy name (Chinese) |
| `signalNameEn` | string | Official strategy name (English) |
| `signalDescCn` | string | Official strategy description (Chinese) |
| `signalDescEn` | string | Official strategy description (English) |
| `createdAt` / `updatedAt` | string | Creation/update datetime |
| `lastSignalTokenTime` | number \| null | Last signal token timestamp (ms) |

---

## `baw signal credits` — Query Credits

```bash
baw signal credits --json
```

### JSON Output

```json
{
  "success": true,
  "data": {
    "balance": "number",
    "dailyLimit": "number",
    "totalVolume": "number",
    "isWhiteList": "boolean"
  }
}
```

Check `balance` before triggering backtests. If `balance` is 0, inform the user that daily credits are exhausted (resets next day).

---

## `baw signal wallet-group` — List Wallet Groups

```bash
baw signal wallet-group -c 56 --json
```

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `-c, --chain-id` | string | yes | Chain ID |

### JSON Output

```json
{
  "success": true,
  "data": [
    { "groupId": "number", "groupName": "string", "addressCount": "number", "displayOrder": "number" }
  ]
}
```

Used to resolve wallet group IDs. Strategy creation (which used `--wallet-group-id`) is DISABLED in this modified skill.

---

## Strategy Type Reference

| Type | Alias | Description | Wallet Group Required |
|------|-------|-------------|----------------------|
| `meme-rush` | `meme` | Early golden dog detection | No |
| `fomo-call` | `fomo` | Follow smart money calls | No (config has `selectedGroups`) |

**fomo-call limitations**: fomo-call does NOT support `backtest retry` (13323027) or `backtest schedule set` (13323006). `schedule/query` (read-only) is supported. Strategy management operations (create/update/delete/follow/unfollow) are DISABLED in this modified skill.

---

## Error Codes

| CLI Error Code | API Code | Description |
|----------------|----------|-------------|
| 1001002 | — | Invalid params (e.g. `--page-size` > 100 → "Invalid page size: 101") |
| 60002001 | 13323005 | Strategy not found |
| 60002002 | 13323006 | Not strategy owner |
| 60002003 | 13323010 | Daily signal limit reached |
| 60002004 | 13323011 | Backtest credits exhausted |
| 60002005 | 13323026 | Strategy count limit reached (stop following to enable new) |
| 60002006 | 13323028 | Service temporarily unavailable |
| 60002007 | 13323031 | AI analysis unavailable |
| — | 13323038 | Strategy not found — returned as raw code with no human-readable message for some commands (e.g. `backtest detail`) |
| — | 13323036 | count-signals incomplete — cannot run update-single (estimate must finish first) |
| — | 13323012 | Empty config `{}` for meme-rush — use a real config with filter params |
| — | 13323027 | Operation not supported for fomo-call type (retry) |
| — | 13323006 | Not strategy owner — also returned when setting schedule on fomo-call |

**Note on error precedence**: `delete` and `retry` with a nonexistent jobId typically return `NOT_OWNER` (60002002), not `NOT_FOUND` (60002001) — the backend checks ownership before existence.

### Gold/Silver/Bronze Definitions

| Level | Condition | Meaning |
|-------|-----------|---------|
| 🥇 Gold | maxGain > 5x | High-quality signal |
| 🥈 Silver | maxGain 3–5x | Medium quality |
| 🥉 Bronze | maxGain 1–3x | Valid signal |
| Zero | maxGain < 1x | Invalid signal |

Gold% + Silver% + Bronze% + Zero% = 100%. The API does not return `zeroRate` — compute it as `1 - goldenRate - silverDogRate - bronzeDogRate`.
