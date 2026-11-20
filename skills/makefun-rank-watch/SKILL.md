# Watch make.fun ranks and results

## Check status first

- Run the kit status command from the free-model-aggregator kit directory to read all entries at once, and read a single entry with makefun status --submission <id>.

- Treat the submission quota as 3 TOTAL per competition with no daily reset; preserve one slot for the final improvement.

- Run `makefun init` first and verify that LICENSE contains `SPDX-License-Identifier: MIT` before interpreting a submission result.

- Run `makefun fee show <slug>` before `fee pay` and report a missing `pay_entry_fee` scope as an account-owner action.

- Verify the entry's live server status before reporting it as submitted — the user cross-checks the make.fun UI.

- Treat status as ground truth for whether an entry is scored, submitted, rejected, or held, and read prizes to claim and prizes won from the same output.

## Read the leaderboard carefully

- Fetch the public dev leaderboard at GET https://make.fun/api/competitions/<slug>/leaderboard with phase=dev, view=performance, and rows=first for the top or rows=all for full values.

- Use /live for a live race and /api/profiles/<handle> for one account.

- The leaderboard API sometimes omits entries that are still ranked, so when an entry disappears from the API but status says it is scored and the site's own notifications still rank it, trust status and the notifications, not the API.

- Ranks slip slowly as new entries arrive while a score stays fixed. That is board mechanics, not the entry weakening, and it is not a loss.

- Klasifikasikan tiap perubahan peringkat sebagai pilihan tertutup — naik / tetap / turun — beserta tingkat keyakinanmu (Decisions API, Nov 2026: skor pilihan tertutup dengan probabilitas dan confidence). Bila keyakinan rendah (mis. entry hilang dari API, angka tidak konsisten antar sumber), jangan laporkan perubahan peringkat sebelum cross-check dengan `makefun status` dan notifikasi situs; laporkan pembacaan itu sebagai belum terverifikasi.

- Dev ranks are provisional, and the final phase re-grades, so a dev rank never decides a prize.

## Know the bars before promising a rank

- Fetch the live board around the target rank and read the score, calls, or judge rate the bar actually needs before promising any rank push.

- A top rank can be mathematically closed, for example when every seat at the minimum possible value is already taken and earlier receipt wins ties. Say so plainly with the measured numbers instead of attempting the impossible.

- Report a win in the user's chat the moment the prize watch or a status check shows a prize claimable or a final result arrived, and never send routine nothing-new reports.

- Never print or send the make.fun API key, keypair, or claim code; keep claim codes only in the bounty NOTES.md.

## Monitoring reliability (agent best practices, 2026)

- **Validate every reading before reporting it.** A status or leaderboard result only counts if you read its full output. If the leaderboard omits an entry, cross-check with `makefun status` and the site's notifications before concluding anything. Never report a rank change from a single incomplete read.

- **Bounded retries with diagnosis.** Status commands can be slow; if one times out, retry once and read the error. If it fails twice, report the check as unverified rather than guessing the rank.

- **Cache stable context.** Ranks and scores change slowly; do not re-fetch the same board every few minutes. Record the last verified reading with its timestamp and reuse it until a new check is actually needed.

- **Keep a reading trail.** Record each rank/status reading with its time, source (status vs leaderboard vs notification), and value. A trail makes a real movement distinguishable from an API omission.

- **Use the CURRENT kit level.** Never use an old kit record command: it may miss Muse sessions and OVERWRITE ~/.makefun/recordings.json, deleting other recordings' local receipts.

- **Know the strict-transcript recording rules.** A recording must start within 300 seconds of the controlling session, exclude the parent session, keep a short window, kill the recorder before `record --finish`, and only a recording with a valid local receipt (matching site-seal and local chunk heads, current format) can be submitted.

- **Run prize checks every 12 hours** from ~/workspace/makefun/prize-watch/state.json and message only claimable prizes or final results, between 06:30 and 21:30 WITA.

- **Join every newly detected contest automatically** (standing order) and record handled slugs in the known-slugs file.

- **Keep leader-only learning with the main agent.** Claude/Grok intelligence and Cyber Defender discipline are never forwarded to clones, builders, or subagents.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.
