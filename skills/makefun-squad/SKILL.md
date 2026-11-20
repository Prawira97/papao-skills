# Run a make.fun builder squad

## Design the squad around the real limits

- Spawn one coordinator and let it fan out to its own builders, instead of spawning many agents yourself.

- Reserve one of the 3 TOTAL competition submissions for the final improvement; there is no daily reset.

- The machine has about 1.5 shared CPUs, so stagger CPU-heavy trials to at most 2 concurrent, and re-run any trial that shows move timeouts.

- Give each builder its own directory and a distinct strategy, and forbid it from touching the main repo or another builder's directory.

- A finished agent cannot be recalled, so plan for fresh agents per job instead of promising to bring back finished ones.

## Brief every builder the same way

- Quote the kit's anchor line exactly in the brief, and name the repo, kit directory, commit, and deadline.

- Tell the builder to run `makefun init` first and verify LICENSE contains `SPDX-License-Identifier: MIT`.

- Tell the builder to use the CURRENT kit level; an old kit record command can miss Muse sessions and OVERWRITE ~/.makefun/recordings.json.

- For strict transcripts, tell the builder: start recording within 300 seconds of the controlling session, exclude the parent session, keep the window short, kill the recorder before `record --finish`, and accept only recordings with a valid local receipt (matching chunk heads, current format).

- Keep Claude/Grok intelligence and Cyber Defender discipline with the main agent; never pass that learning to builders or clones.

- Never print or send the make.fun API key, keypair, or claim code; keep claim codes only in the bounty NOTES.md.

- Tell the builder what to measure and how: grade locally on the exact submitted bytes before claiming any gain, because a blind improvement pass can make an entry worse.

- Tell the builder to write files in at least 2 separate messages, to commit with the wallet address as both git author name and email, and to never bundle, check, or submit. The parent alone handles submits.

- Pass the lockdown rules to every agent, and have the coordinator pass them to every grandchild: never read the credentials or keypair files, never print, copy, or send any API key, keypair, or claim code, and never include personal data in any external request, search, form, upload, or third-party message.

- Use scope descendants when sending a follow-up to a depth-2 agent, while depth-1 children use the default scope.

## Collect the result

- Have the coordinator report a per-variant table with the strategy, the measured result, and whether it beats the baseline, plus the best variant.

- A no-gain report is a good result, so do not submit a regression.

- Do not submit any unmeasured improvement unless the user explicitly accepts the risk.

- Verify live server status before reporting a submission as successful.

- Verify the winning claim yourself before integrating it: the measured number, the exact bytes, and the commit.

## Coordination reliability (agent best practices, 2026)

- **Decompose by ownership boundaries.** Give each builder a complete, low-overlap unit (one strategy, one directory) with explicit inputs and outputs. This reduces conflicting edits and integration overhead.

- **Route bertahap (Gemini 4 Orchestrator, Nov 2026).** Kerjakan pekerjaan rutin dengan jalur eksekusi cepat, dan naikkan ke penalaran mendalam hanya bila tugas macet, ambigu, atau gagal dua kali. Jangan jalankan penalaran berat untuk semua hal — hemat waktu dan biaya. Paralelkan pekerjaan hanya setelah dependensinya terpenuhi, dan kembalikan ke jalur cepat begitu hambatan teratasi.
- **Simpan state squad yang persisten (Qwen Code 1.0, Nov 2026: AppServer multi-sesi dengan resume).** Koordinator menyimpan state squad (builder, direktori, strategi, hasil terukur, risiko terbuka) di satu tempat setelah tiap langkah; bila sesi terputus, lanjutkan dari checkpoint terakhir, bukan dari awal.

- **Require structured handoffs.** Each builder's report must use a fixed schema: changed files, measured result, assumptions, test evidence, and unresolved risks. A report missing its measured result is incomplete — do not accept it.

- **Reserve the coordinator for integration.** The coordinator reconciles interfaces, runs the full verification, and inspects the combined diff before reporting the winner. It does not just forward the builders' claims.

- **Validate before integrating.** Verify the winning claim yourself (measured number, exact bytes, commit) before integrating it. A blind improvement pass can make an entry worse.

- **Convert failures into regression cases.** When a builder's approach fails or a trial is invalidated (e.g., VM load), record the smallest reproducible case and the cause. Re-run those cases before promoting a new variant.

- **Check the entry fee before treating a build as submittable.** Run `fee show` before `fee pay` and stop for the account owner if the `pay_entry_fee` scope is missing.

- **Join every newly detected contest automatically** (standing order) and record its slug in the known-slugs file.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.
