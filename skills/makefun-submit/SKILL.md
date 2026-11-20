# Submit a make.fun entry

## Before you spend a submission slot

- Check the effective quota first: the cap is 3 submissions TOTAL per competition, not the documented 5 and not per-day — there is NO daily reset. A 4th attempt is refused with HTTP 429 and the server says no retry can pass before the deadline.

- Never burn the last slot early — once 3 are used, that competition is closed for good.

- Keep one slot in reserve for a final improvement, and never submit a change that cannot be measured locally unless the user explicitly accepts the risk.

- Confirm the entry passes its local checks and the deadline is still ahead, because the last submission before the deadline is final and each resubmission supersedes the previous submission id.

- Download the CURRENT kit and check its level before running any kit command; an old kit cannot see Muse app sessions and its record command OVERWRITES ~/.makefun/recordings.json, deleting other recordings' local receipts.

- Run `makefun init` FIRST, before any other kit command, and confirm the repo LICENSE contains `SPDX-License-Identifier: MIT` (a missing SPDX line caused a rejection on license_osi).

- Check the entry fee with `makefun fee show <slug>` (positional only). If unpaid, pay with `makefun fee pay <slug> --keypair <file>`; if payment fails with HTTP 403 (AGENT_SCOPE), the API key lacks the `pay_entry_fee` scope and only the account owner can enable it.

## Bundle the transcripts

- Run every kit command from inside the unpacked kit directory, because the bundle command takes no --kit flag.

- Collect the session JSONL for every agent session that wrote entry code, plus fresh usage rows from muse.db with the agent_message_token_usage query, written one JSON object per line.

- For a grandchild or direct-child builder, copy its session JSONL into the bounty directory first, then pass that path, and add --prompt-file with the user's exact words that started the run, --prompt-origin handed-off, and a one-line --prompt-via of 300 characters or fewer naming how the run was handed off.

- Bundle submits take NO run-record flags: do not pass --harness, --harness-version, --provider, --model, --effort, or --mcp when submitting a bundle. Pass --muse-usage <file> only with bundle or transcript submissions — it does NOT apply to recording submits.

- Keep the repo's git author name and email both exactly the payout wallet address, write entry files in at least 2 separate messages, and never copy them from the kit starter, or the duplicate snapshot check refuses the entry.

## Record strict transcripts

- Start recording within 300 seconds of the controlling session's start, or the transcripts_witnessed gate fails.

- Keep the parent session OUT of the recording.

- Keep recording windows short.

- KILL the recorder and confirm it is gone BEFORE running `record --finish`; never pipe finish through `head`.

- Only use a recording with a valid local receipt: reject one whose site seal and local state disagree on the chunk head, and reject old-format receipts.

## Check, submit, record

- Run the kit check from inside the kit directory with --kit. --repo <repo> --transcripts <bundle>, and require all checks to pass with 0 failed.

- Submit from inside the kit directory with --competition <slug> --source <repo> --commit <sha> --bundle <bundle> --title "<title>" --keypair /home/hatch/workspace/makefun/makefun-keypair.json. For a recording submit, use --recording <ids> --source <repo> --commit <sha> --title "<title>" --keypair <file> --mcp none --harness Muse --harness-version muse-spark-1.3 --provider meta --model muse-spark-1.3 --effort default instead.

- The parent alone executes submissions; builders never submit.

- Confirm the entry's LIVE server status before reporting it as submitted — the user cross-checks the make.fun UI and sends screenshots when a Fix-and-resubmit button is still showing.

- Status commands can be slow, and a silent timeout does not mean failure, so retry once before concluding anything.

- Write the submission id and the claim code only in the bounty's NOTES.md under ~/workspace/makefun/<slug>/, and never put a claim code in chat or memory.

- Update the prize-watch baseline at ~/workspace/makefun/prize-watch/state.json with the new submission id and status.

## Push an entry secret

- Push a provider key as an entry secret with the kit's secrets push command, passing the value through exec stdin ONLY — never as a command argument, never in an env file, never in a file at all. The committed-secret scan reads the entry's whole git history in every encoding, so the key must never enter the repo history.

- The Secure Vault never reveals a stored value back, so it cannot feed a secrets push. The working path is the user pasting the key once and piping it through exec stdin, never in a command string or a file.

## Reliability (agent best practices, 2026)

- **Validate every tool result before continuing.** After each kit command, check its exit code and read its full output. A silent timeout or an empty result does not mean success — verify the bundle file exists and has a nonzero size, the check reports 0 failed, and the submit returns a submission id. Never treat a command that produced no output as done.

- **Bounded retries with diagnosis.** If a kit command fails or times out, retry at most once, and only after reading the error. Classify the failure first: transient (network, timeout) → retry once; authorization (403, scope) → stop and report (only the owner can fix it); input (bad flag, missing file) → fix the input, do not retry the same call; state (quota reached, already submitted) → stop, the slot is spent. Never loop blindly.

- **Checkpoint after each step.** Record progress after every successful step (bundle path + sha, check result, submission id) in the bounty's NOTES.md before moving to the next step. If a later step fails, resume from the last checkpoint instead of redoing the whole flow.

- **Keep a persistent submit state (Qwen Code 1.0, Nov 2026: AppServer keeps multi-session state and resumes).** The NOTES.md checkpoint is the session state — quota used, bundle sha, check result, submission id. After any interruption or timeout, read the checkpoint first and reconcile the LIVE server status before retrying anything, so a submit that timed out silently is never sent twice and a spent slot is never re-spent.
- **Test new kit or preview flows in a scratch copy only; production submits run only on the current stable kit level.** A preview branch may change interfaces and has no benchmark backing — never let it touch the live submission path.

- **Keep an evidence trail.** For every submit, keep the bundle path, the check output, the submit command's full output, and the status check result. If the server later disputes the entry, the trail is the evidence.

- **Never print or send the make.fun API key or keypair.** Keep both out of chat, files, logs, and external requests. The parent alone handles submits.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.
