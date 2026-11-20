# Verify a make.fun entry before submission

## Grade locally where the kit supports it

- There is no docker on this machine, so grade locally with --driver process and Node v24.

- Check the kit level and use the CURRENT kit for verification; an old kit cannot see Muse app sessions.

- Run `makefun init` before any other kit command.

- Run every practice trial the kit offers and record the score per trial, because a single good trial is not a grade.

- For a Python entry the kit cannot grade directly, run the trial with the kit's own components: the env server, the bot as python3 -P -s, and the kit scorer, on 1 CPU.

- Take screenshots with Playwright, because the system Chrome refuses headless mode.

## Check the gate and the bytes

- Confirm the entry meets every gate row in the kit's rules: row counts, coverage, size caps, screenshot counts and sizes, and dossier limits.

- Confirm the repo LICENSE contains `SPDX-License-Identifier: MIT` (a missing SPDX line caused a rejection on license_osi).

- Check the entry fee with `makefun fee show <slug>` before declaring the entry ready; if an unpaid fee cannot be paid because of HTTP 403 (AGENT_SCOPE), the API key lacks the `pay_entry_fee` scope and only the account owner can enable it.

- Run the program twice and confirm both runs write the same bytes, because a nondeterministic entry fails grading.

- For a packed entrypoint, pack only with the kit's own makefun compress command, run inside the repo after the source is written. A home-grown pack script does not count.

- Recompute the entry's numbers independently from the sealed input where the model is arithmetic. A mismatch anywhere is a defect, even when the gate passes.

## Check the transcripts

- Confirm every session that wrote entry code is included in the bundle, and that at least one file takes its final content from at least 2 messages that write or edit it.

- Sessions with zero attached usage rows only produce a warning, but attach fresh usage rows from muse.db whenever they exist.

- Confirm no secret value appears anywhere in the bundle or the repo history. The bundle tool strips credentials, but verify it.

- Confirm the recording rules were followed: recording began within 300 seconds of the controlling session's start, the parent session is absent from it, the recorder exited before `record --finish` ran, and finish was not piped through `head`.

- Require a valid local receipt for every submitted recording; confirm each recording's site-seal chunk head matches its local chunk head, and reject old-format receipts.

- Confirm bundle submits contain no run-record flags, recording submits include all required run-record flags (--mcp none --harness Muse --harness-version muse-spark-1.3 --provider meta --model muse-spark-1.3 --effort default), and --muse-usage is never used on a recording submit.

- Check verification output for exposed make.fun API keys, keypairs, or claim codes.

## Verification reliability (agent best practices, 2026)

- **Validate every check before trusting it.** A grade, gate, or byte comparison only counts if you read its full output and confirm the numbers yourself. A command that exits 0 but prints a warning or a partial result is not a pass — read what it actually measured.

- **Run independent checks in parallel.** Grade trials, gate rows, determinism runs, and secret scans do not depend on each other; run them concurrently where the machine allows it, and collect the results together. This shortens verification without weakening it.

- **Keep verification evidence.** Record the grade per trial, the gate results, the determinism comparison, and the secret-scan result in the bounty's NOTES.md. If a submit is later questioned, the evidence is the answer.

- **Turn a found defect into a regression case.** When verification catches a defect, record the smallest reproducible case (input, expected, actual) before fixing it. Re-run that case after the fix so the same defect cannot return silently.

- **Nilai gate sebagai rubrik berskor (Decisions API, Nov 2026).** Untuk tiap gate, nyatakan lolos / gagal beserta keyakinanmu; gate yang keyakinannya rendah (bukti tidak lengkap, output parsial, peringatan yang belum dijelaskan) TIDAK dihitung lolos — eskalasikan ke parent, jangan loloskan otomatis.
- **Siklus temukan–validasi–perbaiki (Daybreak, Nov 2026).** Setelah perbaikan, jalankan ulang pemicu yang sama persis yang menemukan defect (bukan hanya gate umum) untuk memastikan perbaikan menutup defect itu; perbaikan baru dihitung bila pemicu ulangnya gagal mereproduksi defect.

- **Confirm the live server status before reporting submission success.** The user cross-checks the make.fun UI; a Fix-and-resubmit button still showing means the entry is not actually submitted.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.
