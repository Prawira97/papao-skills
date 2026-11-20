---
name: self-improvement-loop
description: Turns finished work into reusable skill for the next task.
version: 2.0.0
author: Papao
license: MIT
---

# Self-Improvement Loop Skill

Turns finished work into reusable skill, so the next session starts already knowing what this one learned. Adapted from the Hermes Agent background review fork (Nous Research, `agent/background_review.py`, commit `6af9d21a`): Hermes spawns a fork after every ~10 tool-calling iterations that replays the conversation and writes durable facts to memory and skills. Papao has no fork, no background pass, and no auxiliary model — the loop is an explicit end-of-task procedure run by the agent doing the work. It does not auto-write anything; structural changes need authorization.

## When to Use

Run the loop at the end of every substantive task:
- A bug-bounty wave (after the verdict), a make.fun entry (after submit), a skill audit or install, a research arc, a debugging session, a Codex/Xingchi run.
- For long arcs, run it at checkpoints, not only at the very end: per wave, per program batch, or about every 10 tool-calling iterations of the same arc. A lesson captured late is a lesson reconstructed — and reconstruction is usually wrong.
- Run it immediately when the same mistake, error, or question recurs. Recurrence is proof the lesson was never captured.

Do NOT run it after trivial tasks (a one-line answer, a single lookup). There is nothing to extract, and a pass that manufactures a lesson from nothing is worse than no pass.

## Prerequisites

- Task notes captured during the work (step 1), or the work is still visible in this session. A loop run from end-of-day memory alone is unverified — say so.
- The skill file to be patched can be re-read fresh in this run (read-before-write, step 4).
- The parent is the authorizer for structural changes (see Approval boundary).

## How to Run

1. Capture during the task (notes at the moment, not from memory later).
2. Scan for signals (below) and extract with the 3 questions.
3. Decide where each lesson lives (decision table, one home only).
4. Write it as a rule (lessons, not logs; read-before-write; fix in place).
5. Report what was learned (every skill created/patched, one line each).

## Quick Reference

**Signals that warrant a skill update (any one is enough):**
- The user corrected style, tone, format, legibility, or verbosity ("stop doing X", "too verbose", "don't format like this", "just give me the answer", "you always do Y and I hate it", explicit "remember this"). Frustration is a FIRST-CLASS skill signal, not just a memory signal.
- The user corrected the workflow, approach, or sequence of steps.
- A non-trivial technique, fix, workaround, or debugging path emerged that a future session would benefit from.
- A skill that was loaded or consulted turned out wrong, missing a step, or outdated — patch it NOW.

**Preference order — take the earliest that fits:**
1. Patch a currently-loaded skill (the one in play this task).
2. Patch an existing umbrella skill that covers the class.
3. Add a support file under an existing umbrella (`references/<topic>.md` for topical depth, `templates/<name>` for starter files, `scripts/<name>` for re-runnable checks). Extend an existing topical file before creating one.
4. Create a new class-level skill — only when nothing covers the class.

**Memory routing — one fact, one store, never both:**
- `~/USER.md`: who the user is — persona, preferences, communication and work style, expectations of behavior.
- `~/MEMORY.md`: facts about the environment — tool quirks, project conventions, config gotchas, paths and totals that matter.
- A style/workflow preference the user expressed belongs in the governing SKILL, not in memory. Memory says who the user is and what the situation is; skills say how to do this class of task for this user. A preference lives in exactly one place: the governing skill when one exists, `~/MEMORY.md`/`~/USER.md` only for cross-cutting preferences no skill owns — never both.
- Save only facts GROUNDED in this conversation — a user message or tool result you can point to. Never infer the user's traits, skill level, role, or mood from topic, tone, or tools used, and never turn a one-off request into a standing preference unless the user marked it general ("always", "from now on", "remember") or stated a standing like/dislike. If unsure, leave it out — a wrong fact misleads every future session.

**Do NOT capture as a skill:**
- Environment-dependent failures (missing binaries, fresh-install errors, path mismatches after a migration, "command not found", unconfigured credentials, uninstalled packages). The user can fix these; they are not durable rules.
- Negative claims about tools ("the browser does not work", "X tool is broken"). These harden into refusals the agent cites against itself for months after the actual problem was fixed. If a tool failed from setup state, capture the FIX (install command, config step) under an existing setup skill — never "this tool does not work" as a standalone constraint.
- Transient errors that resolved before the task ended. If retrying worked, the lesson is the retry pattern, not the original failure.
- One-off task narratives. A single request ("summarize today's market", "analyze this PR") is not a class of work.
- Unresolved failures. If the task ended WITHOUT a working method, do NOT write the failed attempts up as a "reliable workflow". Either save nothing, or capture ONLY an alternative you are independently confident works — never the dead ends, never dressed as best practice.

## Procedure

### 1. Capture during the task, not after it
While working, note in the task notes (wave log, hunt file, `AGENTS.md` draft line) exactly what worked, what failed, and why. Memory of *why* something failed decays within minutes; a note written at the moment is the only reliable raw material. Capture: the failing method + its exact blocker, the working method + its exact command/parameters, and any user correction. Never reconstruct this from memory at the end of the day.

### 2. Extract at the end of the task (3 questions)
- **What would I do differently next time?** (A procedure change, a different tool first, a check done earlier.)
- **What procedure is now proven?** (A sequence that worked end-to-end and is worth repeating verbatim.)
- **What pitfall cost time?** (A dead end, a wrong assumption, a tool quirk — with its mechanism, not just its symptom.)
If none of the three has a concrete answer, there is nothing to extract — stop here. "Nothing to save" is a real option, but it is not the default: be ACTIVE and scan the signals first; a pass that does nothing after a session with corrections is a missed learning opportunity, not a neutral outcome. Never manufacture a lesson to fill the pass.

### 3. Decide where the lesson lives (decision table)
| Lesson shape | Put it in |
|---|---|
| A reusable procedure for a class of tasks (hunt a program, submit an entry, audit a skill) | A skill (`~/workspace/custom-skills/<name>/SKILL.md`) — patch the loaded/umbrella skill first (preference order above); create new only if nothing covers the class |
| A style, format, or workflow preference the user expressed | The skill that governs that task (see memory routing above), NOT `~/MEMORY.md` |
| A durable fact about the user, a program, a deadline, a total | `~/MEMORY.md` (curated, tight) or the task archive (e.g. `valid-findings-archive.md`) |
| A workspace convention or a mistake not to repeat | `~/AGENTS.md` (short, durable) |
| A one-off detail (a submission ID, a file path, a log line) | The task's own notes/log file — NOT a skill |
| Nothing generalizable | Nowhere — drop it |

One lesson, one home. Never copy the same lesson into two places; duplicates drift.

### 4. Write it as lessons, not logs
- **Procedure first.** Steps in the order they are done, with concrete commands, tool calls, and decision points. Lessons and pitfalls attach to the step they affect.
- **A pitfall is a generalizable rule + one clause of WHY** (the mechanism), imperative. Not a narrative of what happened this session.
- **No incident narration.** No story of what happened, no PR/issue numbers, no dates, no quoted chat inside a skill. Dates and IDs live in the report/archive, not in the skill. Keep a short quote ONLY when the quote itself is the clearest statement of the rule.
- **The same lesson twice is ONE rule.** Before adding, search the skill (and its `references/`) for the rule already stated; strengthen or clarify it rather than appending a second copy.
- **Never restate what is already loaded every turn.** Do not copy `~/AGENTS.md`, `~/MEMORY.md`, or tool schemas into a skill. A skill carries the workflow and the pitfalls; it does not restate the codebase map or a tool's parameter list.
- **Always-on rules live in `SKILL.md` itself.** `references/` holds a small set of files named by topic (a decision table, a recipe, provider quirks) — extended in place, never one file per session. A skill with dozens of one-off reference files is the failure shape, not the goal.
- **Fix the skill in place when it is wrong.** Edit the sentence that misled; do not append "UPDATE: actually..." underneath it.
- **New skill names are class-level.** Never a PR number, error string, feature codename, or "fix-X / debug-Y" session artifact. If the name only makes sense for today's task, the lesson belongs in an existing skill instead.
- **New skill description: ≤60 characters, one sentence, ends with a period.** State the capability, not the implementation; no marketing words ("powerful", "comprehensive", "seamless", "advanced"); do not repeat the name or the category.
- **Read-before-write (ENFORCED).** Before patching an existing skill, re-read its `SKILL.md` fresh in this run (`muse.read`); before overwriting an existing support file, re-read that exact file. Content quoted earlier in the session does NOT count. If a patch fails on a stale read, re-read once and retry once; do not loop.
- **Verify before claiming improvement.** A blind improvement pass without a local grade can make things worse (token radar v3: judge 82.5% → 80.1%). If the lesson changes a procedure with a measurable outcome, test it (replay the procedure, run the check) before writing it as the new rule. If it cannot be tested, mark it as untested in the skill and say so in the report.

### 5. Report what was learned
The final report names every skill created or patched and the one-line lesson each carries. Never silently rewrite a skill the user relies on — the report is the notice. If a proposed lesson is structural (a new skill, a merged skill, a changed severity rule), it is proposed in the report and applied when the task authorizes it (see Approval boundary).

## Worked example — the clipboard lesson (as the loop should have run it)

Task: create an API key for the aggregator entry in the browser, then use it.
1. **Capture (during).** Failing method: after creating the key and clicking "Copy key to clipboard", repeated browser rounds tried to read the key back — clipboard paste blocked, DevTools console did not open, right-click menu did not appear. Working method: the user pastes the key once himself. User correction: he stopped the paste attempts — the rounds were the waste, not the key.
2. **Extract.** Differently: stop after the first failed read-back and ask the user to paste once. Proven: create key → click Copy → user pastes once. Pitfall: burning rounds retrying an unrecoverable read-back (mechanism: the browser cannot read the clipboard back).
3. **Decide.** A browser limitation + a mistake not to repeat → `~/AGENTS.md` (workspace convention). One home only; the key's own name and ending live in `~/MEMORY.md`, never in the rule.
4. **Write.** Rule + mechanism, imperative: "The browser cannot read the clipboard back — create the key, click Copy, and have the user paste it once; never burn rounds retrying." NOT written: "the browser is broken" (a negative tool claim that would harden into a refusal), and no date, key name, or quoted chat in the rule.
5. **Report.** The final report named the `~/AGENTS.md` line added. Verification: the next key creation follows the rule on the first try instead of burning rounds.

## Pitfalls
- **Extracting from memory instead of notes.** The lesson as remembered is usually the wrong lesson. If it was not captured during the task, treat it as unverified and say so.
- **Logging the incident instead of the rule.** "The browser could not read the clipboard" is a log line. The skill is: "The browser cannot read the clipboard back — have the user paste the key once; do not burn rounds retrying." Write the second one.
- **A lesson per session.** A skill with 60 reference files or a 24k-char body is a dumping ground, not a skill. Fold new material into the existing structure; if the skill keeps growing, split it by task class instead.
- **Improving without a grade.** Never resubmit or re-advise on the basis of an unmeasured change. The loop improves the procedure; the grade decides whether the improvement ships.
- **Learning the wrong thing from a success.** A task that succeeded by luck (a guess that happened to work, a flaky check that passed) teaches nothing. Only procedures that worked for a stated reason get written down.
- **Writing a negative tool claim.** "Tool X does not work" becomes a standing refusal long after the fix. Write the working alternative, or nothing.
- **Dressing up dead ends.** Failed attempts from a task that ended without a working method are not a workflow. Never present them as one.
- **Duplicating the lesson.** The same rule in a skill and in `~/MEMORY.md` drifts. One home; the other place gets at most a pointer.

## Ambiguous cases
| Case | Decision |
|---|---|
| Lesson fits two homes (a user preference that is also a procedure) | Governing skill wins; `~/MEMORY.md` gets at most a one-line pointer, never the full rule |
| One message corrected both style and workflow | Two lessons: style → governing skill; workflow → the same skill's procedure, or `~/AGENTS.md` if cross-cutting |
| The fix for a wrong skill is untested | Patch with an explicit "untested" marker; the report says untested; never present as proven |
| A tool limitation has no workaround | Write nothing, or write the working alternative if one exists — never "tool X does not work" |
| The task succeeded by luck or a flaky check passed | No lesson; luck is not a procedure |
| The lesson already exists in the skill | Strengthen the existing sentence; do not append a duplicate |
| The lesson is a one-off fact (ID, path, total) | Task log / archive / `~/MEMORY.md` — never a skill |
| Unsure whether a preference is standing or one-off | Leave it out; a wrong standing fact misleads every future session |
| User said "remember this" explicitly | Standing preference → `~/MEMORY.md` (cross-cutting) or governing skill (task-specific) |
| Two skills overlap and both were in play | Patch the one that was loaded first; note the overlap for `skill-curator` |

## Approval boundary
- **Apply directly:** typo fixes, one-line clarifications, and patches to a skill created in the same task.
- **Propose first, apply on authorization:** a new skill, a merged/renamed skill, any change to a severity/reward rule, any change to a skill the user explicitly ordered or relies on (e.g. `skill-safety-checker`, `makefun-submit`, `problem-solving`).
- **Never:** edit a skill the user said not to touch; write a secret, key, token, seed phrase, or claim code into any skill; present an untested change as proven.

## Verification (before finishing)
1. Re-read the skill you created or patched, start to finish. Does it answer "what do I do differently next time?" in one reading?
2. Check it contains no secret, key, token, or claim code, and no incident narration (no dates, no PR/issue numbers, no quoted chat).
3. Check it does not contradict `~/AGENTS.md` or `~/MEMORY.md`. If it does, the older rule wins until the parent decides — note the conflict in the report.
4. Check the decision table: is this lesson in exactly one home?
5. Read-before-write honored: the patch was written from a fresh read of the target file in this run.
6. If the lesson changes a measurable procedure, state the test you ran (or that it is untested).
7. Any new skill's description is ≤60 characters, one sentence, ends with a period, no marketing words, and does not repeat the name.
8. Any new skill's name is class-level, not a PR number, error string, codename, or fix-X artifact.
9. The report names every skill created or patched and its one-line lesson.

## Origin
Adapted from Hermes Agent (Nous Research, MIT), commit `6af9d21a3ab91b78778d9ab197bbbe437606797c` (2026-11-19): background review fork (`agent/background_review.py` — nudge every 10 iterations, fork toolset memory + skills only, max 16 iterations, input budget 75% of context capped at 600k tokens, digest tail 24 messages), `skill_manage` + `/learn`, and the lessons-not-logs authoring standard (`skills/AGENTS.md`). Rebuilt as an explicit end-of-task procedure — no background fork, no auto-writes, no external service. v2 closes the gaps vs the source: memory routing (two stores, grounding rule), signal list, preference order 1–4, read-before-write, do-not-capture list, class-level naming, description ≤60 chars.
