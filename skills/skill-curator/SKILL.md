---
name: skill-curator
description: Keeps the skill library lean, used, and recoverable.
version: 2.0.0
author: Papao
license: MIT
---

# Skill Curator Skill

How Papao keeps the custom-skills library (`~/workspace/custom-skills/`, 156 skill directories) lean, used, and recoverable. Adapted from the Hermes Agent curator (Nous Research, `agent/curator.py` + `agent/curator_backup.py` + `tools/skill_usage.py`, commit `6af9d21a`): Hermes tracks usage per skill and moves long-unused agent-created skills through active → stale → archived on a background pass, never auto-deleting, with snapshots and rollback. Papao has no background pass, so the curator is a periodic manual review run as a task, with the same safety invariants: archive is the maximum, nothing is ever deleted, pinned skills are exempt.

## When to Use

Run a curation review: once a month; when the library feels bloated or two skills clearly overlap; before a big new build that will add skills; after a wave or arc that created skills; or when a skill has not been used in a long time. Do NOT run it in the middle of active work that depends on the skills under review. A review is a task of its own — it reads and proposes, and applies only what the parent authorizes.

## Prerequisites

- The ledger exists (`~/workspace/custom-skills/CURATOR-LEDGER.md`) or is created on this first review.
- `tar` available for snapshots; the parent authorizes the live run (the first pass is always a dry run).
- `cron.list` / hooks / goal workspaces can be checked for skill references.

## How to Run

1. Inventory the library and reconcile the ledger (first sight seeds the clock — never epoch).
2. Update usage (honest counts; judge overlap on CONTENT, never on counters).
3. Scan for prefix clusters; ask the umbrella question; consolidate (merge / new umbrella / demote) or keep.
4. Check package integrity before any demotion or archival.
5. Snapshot the library before applying anything.
6. Dry-run report first (the report IS the deliverable); apply only authorized actions; record every mutation in the ledger with its snapshot id.

## Quick Reference

**Lifecycle (Papao's thresholds — Hermes uses stale 14 days / archive 30 days, reviewed every 7 days after 2 hours idle; Papao's use is bursty, so longer):**
- active → stale: unused for **60 days**.
- stale → archived: unused for **90 days** total.
- archived: directory MOVED to `~/workspace/custom-skills/.archive/<skill>/`. Fully recoverable.
- restore: move the directory back, set status `active`. Refuse if a different skill now occupies the name.
- reactivation: a stale skill used again returns to `active`; record it in the ledger.

**Invariants (hard):**
- Never delete. Archive is the maximum.
- Pinned skills never transition. Protected skills are never archived or absorbed.
- Cron/hook/goal-referenced skills are treated as pinned; a merge is allowed only if the reference is rewritten to the umbrella in the same pass.
- Never touch user-authored skills, system skills (`/opt/muse/skills/`), or any other repo's skills. Only `~/workspace/custom-skills/`.
- Never "improve" a skill during curation — content improvement belongs to `self-improvement-loop`.
- Fail closed: ledger damaged or state undetermined → leave that skill alone, say so.

**Telemetry (per skill, honest counts — Papao has no per-skill meter):**
- `uses` (times the skill drove work), `patches` (times it was patched — churn signal), `last used` (date), `status` (active/stale/archived), `pinned` (yes/no).
- `uses` 0 or 1 is absence of evidence, not proof of disposability. Never archive a never-used skill unless it is at least 30 days old AND its content is genuinely obsolete or fully absorbed elsewhere.
- A `SKILL.md` body over ~24k chars is a consolidation target on its own: distill to always-on rules, push depth into `references/`.

## Procedure

### 1. Inventory
`ls ~/workspace/custom-skills/` (and `.archive/`). Compare against the ledger; add rows for skills missing from it, remove rows for skills that no longer exist anywhere. A skill seen for the first time gets `created` = today — its inactivity clock starts NOW, never at epoch; never archive a skill on its first review. Never-used skills anchor on `created`, so they cannot self-archive.

### 2. Update usage
For each skill, set `last used` / `uses` / `patches` from what the task history shows (memory search, recent wave logs, cron references). Mark the status transition the thresholds dictate — as a PROPOSAL, not an action. Judge overlap on CONTENT, not on counters: do not skip a consolidation because a skill has high uses, and do not propose archival because uses are low.

### 3. Cluster scan and consolidation
1. Scan the full list. Group by prefix / domain keyword (first word or shared domain term). Expect clusters.
2. For each cluster with 2+ members, do NOT ask "are these pairs overlapping?" — ask "what is the UMBRELLA CLASS these skills all serve? Would a human maintainer write this as N separate skills, or as one skill with N labeled subsections?" If the latter, consolidate.
3. Three ways to consolidate — use the right one per cluster:
   a. **Merge into an existing umbrella** — one member is already broad enough. Patch it to add a labeled subsection for each sibling's unique insight, then archive the siblings.
   b. **Create a new umbrella** — no member is broad enough. Write a new class-level skill covering the shared workflow, with short labeled subsections. Archive the absorbed narrow siblings.
   c. **Demote to support files** — a sibling has narrow-but-valuable depth needed only sometimes. Distill it into the umbrella's `references/<topic>.md` (named by TOPIC, merged into an existing topical file when one covers it), `templates/<name>` (starter files), or `scripts/<name>` (re-runnable checks). Then archive the old sibling.
4. Consolidation means DISTILLING: absorbed content becomes rules (imperative + one clause of why); the same lesson stated twice becomes one rule; incident narration, PR/issue numbers, dates, and quoted chatter are dropped — the rule must stand without the story. Moving a file unchanged under `references/` is filing, not consolidating.
5. Re-scan once after the first round's proposals for the next umbrella opportunity, then stop and write the report. Do not manufacture archives: a review that finds zero archives is a valid outcome. (Hermes' background prompt expects "fewer than 10 archives = stopped too early" — that rule is for its automated pass over hundreds of agent-spawned micro-skills and is NOT adopted here. Papao's library is curated; an archive quota would destroy load-bearing skills.)
6. Also flag skills whose NAME is too narrow (a PR number, a feature codename, a specific error string, an "audit" / "diagnosis" / "salvage" session artifact). These almost always belong as a subsection or support file under a class-level umbrella.
7. "Keep" is legitimate ONLY when the skill is already a class-level umbrella and no proposed merge would improve discoverability. "Narrow but distinct from its siblings" is NOT a reason to keep — it is a reason to move it under an umbrella as a subsection or support file.

### 4. Package integrity (before any demotion or archival)
Inspect the skill as a COMPLETE directory package, not just `SKILL.md`. A skill root may include `references/`, `templates/`, `scripts/`, and `assets/`; a reference markdown file inside another skill is NOT a skill root and gets no discovery of its own. If the source skill has support files OR its `SKILL.md` contains relative links (`references/...`, `templates/...`, `scripts/...`, `assets/...`), do NOT flatten only `SKILL.md` into `<umbrella>/references/<old>.md`. Choose one safe path: keep it standalone; fully merge it by re-homing every needed support file into the umbrella's canonical directories AND rewriting the destination instructions to the new paths; or archive the entire original package unchanged. Never leave archived/demoted instructions pointing at files left behind under the old directory.

### 5. Snapshot before mutating
Before applying any archival/merge batch, snapshot the whole library (rollback is itself undoable — snapshot the current tree first, then restore):
```
mkdir -p ~/workspace/custom-skills/.curator_backups
tar -czf ~/workspace/custom-skills/.curator_backups/<YYYYMMDD-HHMMSS>.tar.gz --exclude=.curator_backups -C ~/workspace/custom-skills .
tar -tzf ~/workspace/custom-skills/.curator_backups/<YYYYMMDD-HHMMSS>.tar.gz | head -5   # verify the snapshot lists the skills
```
Record the snapshot id in the ledger mutation lines. The snapshot includes `.archive/` and the ledger; it excludes `.curator_backups/` itself. Rollback: snapshot the current tree first (same command, id `pre-rollback-<YYYYMMDD-HHMMSS>`), then `tar -xzf <snapshot>.tar.gz -C ~/workspace/custom-skills`. All mutations go through the ledger — never a bare `mv` with no ledger entry; an unledgered move breaks rollback the same way it does in Hermes (a snapshot taken after a silent move restores a hollow skill).

### 6. Dry run, then apply and record
1. **Dry run first, always.** The first pass produces the report only — no `mv`, no edits, no ledger status changes. The report IS the deliverable; the parent decides on it.
2. **Propose, do not apply.** The report lists every proposed transition (stale / archive / merge / restore) with its reason, plus the structured summary block below. The parent authorizes; only authorized actions are applied. Archival without authorization is forbidden.
3. **Apply and record.** Move directories, update the ledger (status + dated mutation line with snapshot id), and report what changed. Verify the counts: active + stale + archived (+ pinned, a flag, not a status) must equal the total number of skill directories.
4. **Structured summary (required in every review report — every archived skill in exactly one list):**
```yaml
consolidations:
  - from: <old-skill-name>
    into: <umbrella-skill-name>
    reason: <one short sentence — why merged, not just 'similar'>
prunings:
  - name: <skill-name>
    reason: <one short sentence — why archived with no merge target>
```
Leave a list empty (`consolidations: []`) if none. Do not omit the block.

## The ledger
One file is the source of truth: `~/workspace/custom-skills/CURATOR-LEDGER.md`. Create it on the first review; update it on every review. Format (one row per skill):
```
| skill | created | last used | uses | patches | status | pinned | note |
|---|---|---|---|---|---|---|---|
| problem-solving | 2026-11-16 | 2026-11-19 | 40+ | 3 | active | yes | user-ordered, never archive |
| btc-private-key-recovery | 2026-11-19 | 2026-11-19 | 1 | 0 | active | no | rare but load-bearing; do not churn |
```
- `uses` / `patches` are honest counts from memory and task logs, not a precise meter. "40+" means "used constantly"; "1" means "used once". Never invent a precise number.
- `status` is one of `active` / `stale` / `archived`.
- `pinned` is `yes` only for skills the user ordered, that guard safety (`skill-safety-checker`), or that an active cron/hook/goal depends on. Pinned skills never transition.
- **Protected (never archived or absorbed, patches only via approval):** `skill-safety-checker`, `makefun-submit`, `problem-solving`, `self-improvement-loop`, `skill-curator` itself, and any skill the user explicitly ordered to keep. List them at the top of the ledger.
- Every mutation the curator applies is appended to the ledger as a dated line: `2026-11-19 — archived <skill> (stale 90d, approved by parent, snapshot 20261119-233000) — was: <path>, now: .archive/<skill>/`.

## Worked example — first review of the real library (dry run)
Inventory: 156 skill directories, no `.archive/` yet, no ledger yet. This review creates the ledger and proposes nothing destructive.
1. **Inventory + seed.** All 156 get rows; `created` = today for any skill whose creation date is unknown (clock starts now, never epoch). Nothing can be archived on a first review.
2. **Cluster scan.** Two real prefix clusters surface: `memecoin-*` (3: `memecoin-trading`, `memecoin-analysis`, `memecoin-auto-trader`) and `binance-*` (9: `binance`, `binance-agentic-wallet`, `binance-leaderboard`, `binance-onchain-copy-trader`, `binance-prediction-updown`, `binance-sports-ai-analyzer`, `binance-tokenized-securities-info`, `binance-trading-signal`, `binance-wallet-tracker`).
3. **Umbrella question — memecoin cluster.** `memecoin-trading` is the safety gate; `memecoin-analysis` uses it as a gate for research; `memecoin-auto-trader` uses it as a gate for money-moving execution. Would a maintainer write one skill? No — one file would mix a read-only research procedure with an auto-trade playbook that moves real money under explicit approval. The right shape is a gate + two consumers. Verdict: KEEP all three; record the dependency in the ledger notes (`memecoin-analysis` → gate `memecoin-trading`).
4. **Umbrella question — binance cluster.** Distinct jobs, distinct triggers: `binance` wraps the CLI (Spot/Futures/Convert, needs auth); `binance-trading-signal` is read-only on-chain signals; `binance-sports-ai-analyzer` is World Cup match analysis only. No shared workflow to umbrella. Verdict: KEEP. But the scan flags a quality defect: `binance-trading-signal`'s description is a multi-line paragraph, far over the ≤60-char rule — a patch candidate for `self-improvement-loop`, not an archival.
5. **Staleness check.** `btc-private-key-recovery`: used once, its topic closed by the user. Use=1 is absence of evidence, not staleness; it is young and load-bearing. Verdict: stays `active`; re-check next review.
6. **Snapshot + report.** No archival is proposed, so no snapshot is needed this pass (snapshots are taken before APPLYING a batch, and nothing is applied). The dry-run report carries the structured summary with both lists empty and the ledger file as its deliverable. Outcome: zero archives — valid, not a failure.

## Pitfalls
- **Churning rare-but-load-bearing skills.** A skill used once in a critical moment (`btc-private-key-recovery`, `muse-bug-bounty`) is worth more than a skill used weekly for trivia. Age alone never archives; ask "what breaks if this is gone when it is next needed?"
- **Merging by name similarity.** Two skills with similar names can cover different jobs (`binance` vs `binance-agentic-wallet`; `memecoin-analysis` vs `memecoin-auto-trader`). Merge only when the procedures and triggers actually overlap — read both skills first.
- **Judging overlap on counters.** High uses do not block a merge; low uses do not justify one. Overlap is judged on content.
- **"Distinct trigger" as a keep reason.** Pairwise distinctness is the wrong bar. Ask the maintainer question instead.
- **Flattening a skill package.** Archiving or demoting only `SKILL.md` while its `references/` stay behind leaves instructions pointing at files that no longer exist where they point. Move the whole package or re-home every file.
- **Silent moves.** A bare `mv` with no ledger entry is an unrecoverable action in disguise — the next snapshot restores a hollow skill. Every move is ledgered with before/after paths and snapshot id.
- **Archiving a cron-referenced skill.** A cron job that loads the skill fails on its next run. Rewrite the reference to the umbrella in the same pass, or keep the skill.
- **Ledger drift.** A ledger that is not updated on every review becomes fiction within a month. The review is not done until the ledger is written.
- **Silent archival.** An archived skill that nobody was told about looks like a broken install. Every archival is reported by name, with the restore path, in the same turn it happens.
- **Manufacturing archives.** A review that finds zero archives is a valid outcome. Never archive to hit a number.

## Ambiguous cases
| Case | Decision |
|---|---|
| Two skills share a prefix but do different jobs (gate vs auto-trader) | Keep both; record the dependency in the ledger note; merging would mix safety modes |
| A skill's description is >60 chars or its body is >24k chars | Patch candidate for `self-improvement-loop`, not an archival; note it, do not archive |
| A skill is stale but holds the only copy of a procedure | Keep — or absorb it into an umbrella first, then archive the original; never archive the only copy |
| A skill was used once, in a critical moment, and the topic is closed | Stays active; re-check next review; use=1 is not staleness |
| A skill was never used and is under 30 days old | Leave alone; the clock starts at first sight, not epoch |
| A cron/hook references a skill proposed for merge | Merge allowed only if the reference is rewritten to the umbrella in the same pass; otherwise keep |
| A goal workspace references a skill | Treat as pinned for this review |
| A user-authored skill looks obsolete | Propose only; never touch; the user decides |
| Two skills overlap but each has a distinct trigger phrase | Wrong bar — ask the maintainer question (one skill with labeled subsections, or N skills?) |
| The review finds zero archives | Valid outcome; never manufacture archives to hit a number |
| Ledger damaged or a skill's state cannot be determined | Leave that skill alone; say so in the report (fail closed) |
| A merge would leave references pointing at the old directory | Do not flatten `SKILL.md` only; re-home every support file and rewrite the paths, or archive the whole package unchanged |

## Safety rules (hard)
- **Never delete.** Archive is the maximum. No `rm`, no trash, no "cleanup" that destroys a skill. A deleted skill is unrecoverable knowledge.
- **Never archive a skill an active cron, hook, goal, or running task depends on.** Check `cron.list` / hooks and the goal workspaces first; a referenced skill is treated as pinned for the review. A merge is allowed only if the reference is rewritten to the umbrella in the same pass.
- **Never archive or absorb a protected skill.** Protected list: `skill-safety-checker`, `makefun-submit`, `problem-solving`, `self-improvement-loop`, `skill-curator`, and any skill the user explicitly ordered to keep.
- **Never archive or edit a skill the user wrote or explicitly ordered to keep.** User-authored skills are theirs; the curator only proposes, never touches.
- **Never touch another agent's skills.** Only `~/workspace/custom-skills/` is in scope — never `skills/` or `optional-skills/` of any other repo, never system skills in `/opt/muse/skills/`.
- **Never "improve" a skill during curation.** Curation moves, merges, pins, and archives. Content improvement belongs to `self-improvement-loop`, with its own verification.
- **Snapshot before mutating; rollback is itself undoable.** No batch of archival/merges is applied without a verified snapshot recorded in the ledger.
- **Fail closed.** If the ledger is damaged or a skill's state cannot be determined, leave that skill alone and say so in the report. Do not guess a status.

## Verification (before finishing)
1. Ledger updated: every skill has a row; statuses match the directories on disk; the mutation log lists today's actions with snapshot ids.
2. Counts add up: active + stale + archived = total skill directories (active library + `.archive/`).
3. Snapshot exists and verifies (`tar -tzf` lists the skills); the rollback path is stated in the report.
4. Every archived skill is restorable: its directory exists whole under `.archive/<skill>/` with `SKILL.md` intact; every archived skill appears in exactly one list of the structured YAML summary.
5. No pinned, protected, user-authored, or actively-referenced skill was moved or edited without its reference rewritten.
6. No archived/demoted instruction points at a file left behind under the old directory (package integrity).
7. The report names every transition applied and every proposal left for the parent, with the structured YAML block.

## Origin
Adapted from Hermes Agent (Nous Research, MIT), commit `6af9d21a3ab91b78778d9ab197bbbe437606797c` (2026-11-19): curator lifecycle (`agent/curator.py` — active → stale 14d → archived 30d, never auto-delete, pin/lock, cron-referenced = pinned, protected built-ins, use=0 rules, cluster scan + umbrella question, three consolidation ways, distill-not-file, package integrity, structured summary), snapshots + rollback (`agent/curator_backup.py` — tar.gz + manifest, rollback snapshots current first), telemetry (`tools/skill_usage.py` — use_count, view_count, patch_count, last_activity_at), authoring standards (`skills/AGENTS.md` — description ≤60 chars, section order, ~200 lines complex / ~100 simple). Rebuilt as a periodic manual review with a human-readable ledger file — no background pass, no auto-transitions, no external service. Papao's thresholds are 60/90 days (burst usage); Hermes' "fewer than 10 archives = stopped too early" is NOT adopted. v2 closes the gaps vs the source: cluster scan + umbrella question, three consolidation ways, distill rule, package integrity, snapshot/rollback, structured summary, protected list, reactivation, first-sight seeding.
