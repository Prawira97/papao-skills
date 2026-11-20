# Problem Solving Skill

How Papao unblocks difficult and complicated tasks instead of getting stuck or repeating the same failed approach. Built from real failures (the OpenRouter key saga, 2026-11-16) and the agent-best-practices work (`~/workspace/xingchi-upgrade/agent-best-practices-2026.md`).

## When to use
Use this whenever a task is stuck, has failed more than once, or has several possible routes and no obvious one. Use it BEFORE asking the user for help and BEFORE repeating an approach that already failed.

## The method
1. **Define the real goal, not the method.** The goal is the outcome that matters. A method ("paste the key from the browser") is not the goal — the goal is "get a usable key into the entry secret". When the method fails, the goal stays; only the route changes.
2. **Enumerate every route before trying.** Write down all possible ways to reach the goal: UI, API, clipboard, files, recreating from scratch, user takeover, asking the user. Do this BEFORE spending time on any single one.
3. **Try the cheapest route first.** Cheapest = least time, least risk, most reversible. Timebox each attempt (minutes, not hours).
4. **Verify each result before continuing.** Check what actually happened. Never assume a step worked because it looked right.
5. **On failure, pivot — never repeat the same failed method.** Diagnose WHY it failed, then pick a DIFFERENT route. Repeating the exact same method and expecting a different result is the core failure mode.
6. **Convert failures into knowledge.** Record what was tried, what failed, and why — in the task notes or AGENTS.md — so the next attempt (and the next task) starts smarter.
7. **Escalate with a decision, not an open question.** When only the user can unblock it, tell them the exact one-step action and what happens right after. Never ask the same question twice.
8. **State the leading hypothesis and one falsifiable prediction before testing.** If the prediction fails, the hypothesis is wrong — change the hypothesis, not the test.
9. **Trace repeated failures to their root cause with five whys.** Ask "why?" five times; fix the root cause, not the symptom.
10. **Run a brief pre-mortem before starting a hard task.** Imagine the task has already failed and name the most likely cause; address that cause first.
11. **Timebox each approach, then switch methods when the limit expires.** A timebox that ends with no progress is a signal to pivot, not to extend.

## Stuck protocol (run the moment a task has failed twice)
1. Record the two failed methods and their exact blockers.
2. Identify the shared root cause or missing capability.
3. Remove every route that depends on that same blocker.
4. Choose one different route with a concrete success test.
5. If no viable route remains, state the blocker and hand the user the single required action.

## The 100% correct standard (Prawira's order, 2026-11-16)
Every task is executed to this standard. A step counts only when it is verified; a report contains only confirmed facts; there is no guessing.
- **KECEPATAN (Speed):** take the fast path — a direct API or CLI call instead of the browser when one exists; parallelize independent reads; cache stable context; timebox each attempt and switch methods when the limit expires.
- **KETEPATAN (Precision):** do exactly the right thing — the right tool, the right target, the right parameters; no wasted actions. If a tool cannot do the job, say so instead of forcing it.
- **AKURASI (Accuracy):** verify every result before continuing; never guess or fabricate a value; check before reporting. If it is not confirmed, say it is unverified — do not present it as fact.
- **PERFORMA (Performance):** finish the task fully, not half-done; handle errors properly (classify the failure, retry boundedly with a different remedy, or stop and report); leave the work in a clean, verifiable state with an evidence trail.

## Anti-patterns (from real failures)
- Asking the user the same question 4+ times (OpenRouter key paste, 2026-11-16).
- Trying Ctrl+V, JS clipboard read, and menu paste after the browser already proved paste is blocked — three variants of the same blocked capability.
- Reporting "the browser is stuck" without a new plan.
- Guessing or inventing a value to fill a gap (never guess a secret, key, or code).
- Waiting silently while a deadline approaches.

## Case study: OpenRouter key (2026-11-16)
- **Goal:** get a full OpenRouter API key value to push as an entry secret for aggregator-02.
- **Routes tried:** read the masked dashboard (failed — masked everywhere); clipboard paste in browser (failed — paste blocked); create a new key + copy to clipboard (key created, but clipboard unreadable by the browser); JS clipboard read (failed — no console); menu paste (failed — no menu).
- **What worked:** creating the key and copying it to the clipboard. **What was missing:** a way to read the clipboard back. The only remaining route was the user taking over and pasting — which should have been offered ONCE, clearly, early, instead of after 4+ rounds of asking.
- **Lesson:** when a route's only blocker is a capability the agent lacks (reading the clipboard), say so immediately and hand the user the single step, instead of trying more variants of the same blocked capability.

## Reliability rules (from agent-best-practices-2026)
- Validate every tool result before continuing.
- Bounded retries with diagnosis — never blind loops.
- Make mutations idempotent and checkpointed.
- Keep a plan-state + evidence trail.
- Parallelize independent reads; cache stable context.
- Verify incrementally; stream progress.
