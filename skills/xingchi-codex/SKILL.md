# Xingchi Codex Skill

Use the $1000 Xingchi API credits (Papao's account, yudieprawira97) through Codex CLI to get a second AI model's help — research, review, verification, and drafting — when a second opinion or extra model capacity would improve the work.

## Setup (already done, do not redo unless broken)

- **API key**: named "Papao", stored in `~/.xingchi/api-key` (0600). NEVER print it, never put it in chat, memory, or any file you share. Read it only via `$(cat ~/.xingchi/api-key)` into an env var.
- **Codex CLI**: `/opt/hatch-image/bin/codex`, v0.164.0. Config in `~/.codex/config.toml`:
  - model `gpt-6.1-sol`, provider `xingchi`, base `https://xingchiapi.com/v1`, env_key `XINGCHI_API_KEY`.
  - Official base is `https://api.xingchiapi.com/v1` (also works); switch only if the current base fails.
  - Models available: `gpt-6.1-sol`, `gpt-6-astra`.
- **Helper**: `~/workspace/xingchi-upgrade/codex-xingchi.sh "prompt" [logfile]` wraps the invocation. Run it with `bash` explicitly if direct execution fails with permission denied.

## The only working invocation

```bash
XINGCHI_API_KEY=$(cat ~/.xingchi/api-key) codex exec --approve-for-me --skip-git-repo-check "<prompt>" < /dev/null > /tmp/codex-<name>.log 2>&1
```

Three things are mandatory, learned the hard way:
1. **`< /dev/null`** — `codex exec` reads extra input from stdin and waits forever without it. Every earlier hang was this.
2. **`--skip-git-repo-check`** — Codex refuses to run outside a trusted directory without it.
3. **`--approve-for-me`** — auto-approves requests so a non-interactive run never blocks on a prompt.

## Limitations (do not fight them)

- **Direct API calls are blocked.** The relay returns `client_not_allowed` for curl/SDK. Only coding clients (Codex, Claude Code, Cursor, Cline, etc.) may call it. Never spoof a User-Agent to evade this.
- **Codex cannot write files here.** The code-mode host binary (`/opt/hatch-image/bin/codex-code-mode-host`) is missing, so Codex's file-write tool fails. Ask Codex to PRINT its output as plain text in its response, then save the text yourself from the log. Do not ask it to write a file.
- **`wire_api = "chat"` is invalid** in Codex 0.164 (config fails to load). Leave the default `responses` wire API alone.
- **The official site config** uses provider id `OpenAI`, `experimental_bearer_token`, base `https://api.xingchiapi.com/v1`, and header `x-openai-actor-authorization: local-image-extension`. My env-key config works; use the official one only if mine breaks. Never copy the site's config verbatim into a file, because it embeds the key in plaintext.

## When to use it

- A second opinion on a tricky decision, a code review, or a verification pass.
- Research (best practices, techniques, comparisons) to feed into Papao's own skills.
- Drafting (reports, plans, skill text) that Papao then reviews and saves.
- Never for anything that needs Papao's private data, credentials, or claim codes — keep those out of Codex prompts.

## Cost control

- A short answer costs ~2,800 tokens; a research report ~3,800–9,300 tokens. Latest known balance is $2,999.99 with a concurrency limit of 10 requests; check the dashboard for current usage.

- Use the credits as much as needed for skill upgrades under the user's standing permission ('use them as much as you like'); give every Codex run a clear purpose — no purposeless calls.

## Read results reliably

- Expect the response twice in the log (streaming + final output); read one copy.
- Read usage from the "tokens used" line; do not infer or double-count usage from duplicated response text.
- Check the exit status and the log for errors before treating a run as successful.
