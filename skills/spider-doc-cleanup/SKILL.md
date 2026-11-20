---
name: spider-doc-cleanup
description: "Use this skill when SPIDER protocol project documentation needs archiving or cleanup. This includes removing eligible completed task files, maintaining compact project/task indexes, cleaning up obsolete design.html artifacts, and removing stale SPIDER files from subdirectories while preserving immutable decision history."
---
# Audit note (Papao, 2026-11-20) — AUDITED SAFE

- Source: github.com/Algoza-Solutions/spider-protocol, commit `21950d87d693f1f59ffaf88339c80c2783e3d0f2`, cloned read-only 2026-11-20 to `~/workspace/spider-study/`. Original skill name: `doc-cleanup`. Original SHA-256 of this file: `E5572C772FCA00EFF6CB6C8AAAE300A8CC1337C8A9F1240F46CE9A848111D2A8` (all 21 bundle files matched the repo manifest).
- Verdict SAFE per skill-safety-checker: pure Markdown role contract; no data exfiltration, no credential/token/env access, no network calls, no remote code execution, no instruction to ignore user/system instructions (it explicitly defers to them). No obfuscated code, no base64 blobs. `install.py` was NEVER run; the bundle verifier script was NOT executed (hashes checked independently).
- The `agents/openai.yaml` file is inert Codex display metadata (name + prompt); `references/role-instructions.md` is byte-identical to the source.
- Role contract for documentation cleanup. PAPAO HARD RULE: never delete anything without Prawira's explicit order — findings, reports, and archive entries are only deleted when he says so. Deletion powers here apply only to SPIDER-repo artifacts in their own context.


# Doc Cleanup

Adopt this specialist role for the current request.

## Load the operating contract

Read [role-instructions.md](references/role-instructions.md) completely before taking any task action. Apply it as the role's mandatory operating contract.

- Interpret references to `this agent` as the coding agent instance using this skill.
- Treat source-role boundaries, artifact ownership, state transitions, and exact output contracts as binding.
- Follow system, developer, and explicit user instructions when they override the role contract.
- Use only the portions of the contract relevant to the current invocation, while honoring every prerequisite and guard it names.

## Keep immutable records newest-first

Treat "append" as an immutable addition, not as end-of-file placement. When adding an entry to any append-only SPIDER document, ledger, table, or log, insert the complete new entry before older entries, immediately after the fixed document title and preamble, table header, or owning section heading. This includes `requirements.md`, `decisions.md`, task `## LOG` and `## DEBUG LOG` sections, and equivalent histories. Never reorder, rewrite, or delete existing entries unless an explicit cleanup contract authorizes it.

## Record ISO 8601 timestamps

Every new SPIDER progress/history record that this skill creates or updates uses the actual current time as a second-precision ISO 8601 timestamp with timezone offset (`YYYY-MM-DDTHH:mm:ss?HH:mm` or `Z`). Do not emit date-only output. Preserve historical date-only evidence without inventing times.
