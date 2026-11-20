# Hunt a Muse bug bounty

## Know the tiers and the eligibility line

- Read the payout guidelines at https://bugbounty.meta.com/en-gb/payout-guidelines/muse/ before choosing a target, and confirm the tier definitions and the not-eligible list from that page.

- Confirm current scope, eligible targets, and testing restrictions in Meta's official program rules before each new target.

- Chase the tier whose control you can actually test on your own agent. Tier 7 (bypassing Muse security controls, up to $5,000) is the most reachable. Higher tiers need a control whose bypass escapes the agent or the fleet.

- Skip the dead ends the program already declares not eligible: injection with no outcome, jailbreaks, system-prompt extraction, tool enumeration, installing your own malware in your own sandbox, denial of service, rate-limit bypass, and duplicates of paid findings.

- Remember the victim-interaction ladder: fewer clicks by a victim means a higher payout, and a finding that needs no victim interaction at all pays the most in its tier.

## Map the controls before testing anything

- Map the security controls on the user's own agent first: approval dialogs, Sentinel egress approval, the credential store with surrogate tokens, the prompt-injection defense layers, and OTP redaction.

- For each control, state what it protects and what a bypass would have to demonstrate before you design any test.

- Study the published findings for the pattern: the $300,000 flaw questioned a trusted proxy header, and the $90,000 flaw spoofed tool output. The winning move is finding a trusted assumption and proving it wrong, not brute force.

## Design safe experiments

- Use dummy content only: fictional names, test@example.invalid, TEST-TOKEN-0000 style values. The user's real emails, files, wallet keys, API keys, and tokens never enter a test.

- Test only the user's own agent with dummy data.

- Require explicit authorization for any dummy job creation needed to prove impact; delete the job immediately and verify removal.

- Keep tier-6/5 probes metadata/banner-only, with no writes, tampering, or credential extraction; stop and report before going beyond observation.

- Observe first and act later. Run one experiment at a time, and report the result before the next one runs.

- Stop at the decision point: never complete a send, never create a job or message that moves data, never weaken a protection. If a step risks real data, stop that step at once and report it.

- Run the experiment with a runner agent first, then repeat it on the live agent with the same dummy material, and record both results. Neither run is blind, so call the result a baseline, not proof.

- Record every result in the hunt plan file, including the honest limits and the key points (what held, what did not fire, what is still untested).

## Report a real finding

- Stop all further testing the moment a real bypass appears, and document the exact reproduction steps, the evidence, and the impact on a real user.

- **Siklus temukan–validasi–perbaiki (Daybreak, Nov 2026).** Sebuah temuan hanya dihitung setelah eksploitasinya divalidasi pada reproduksi terisolasi (data dummy, agen sendiri, ruang lingkup yang diizinkan) — bukan dari teori atau satu observasi. Bila temuan menyarankan perbaikan, perbaikan itu diajukan untuk tinjauan manusia dan diuji ulang dengan serangan yang sama untuk memastikan perbaikan menutupnya; tidak ada perbaikan yang diterapkan otomatis.
- **Triage severity sebagai pilihan tertutup (Decisions API, Nov 2026).** Nilai severity sebagai pilihan dari tier yang ada (bukan teks bebas) beserta keyakinanmu; bila keyakinan rendah, perlakukan sebagai lead yang belum terkonfirmasi, bukan temuan — jangan menaikkan severity untuk menutupi keraguan.

- Add reproductions of an already submitted issue to that report; resume testing only within explicitly authorized follow-up scope.

- Report through Meta's official form, one issue per report, and never exploit the finding or disclose it publicly before Meta has time to fix it.

- If you touched another user's data by accident, stop, notify Meta, and delete it.

## Case study — submitted tier-7 chain and exhausted paths

- Track report #4197202927079324 as submitted, status New, awaiting triage; do not describe it as accepted or paid.

- Preserve the tier-7 evidence: scheduled-job creation lacked approval, split content evaded classification, and parameters were entirely content-adopted; the endpoint test created a dummy job and deleted it immediately.

- Record V3 cross-channel splitting as reproducing the submitted chain and V4 as proving payload-only adoption.

- Treat tier-6 Unix-socket probes and tier-5 H5-1 as exhausted at the tested level; reopen only with a new hypothesis supported by evidence.

## Hunt reliability (agent best practices, 2026)

- **Validate every experiment before claiming a result.** A bypass only counts if you can reproduce it with the same dummy material in both the runner and the live agent, and you have the exact steps and evidence. A single unreproduced observation is a lead, not a finding.

- **Keep a complete evidence trail.** Record every experiment (hypothesis, method, result, limits) in the hunt plan file as it happens, not from memory afterward. If a finding is later questioned, the trail is the proof.

- **Turn a non-reproduction into a regression case.** When an experiment that should have worked does not reproduce, record the exact setup and the difference. That record prevents re-testing the same dead end and sharpens the next hypothesis.

- **Bound each experiment.** Run one experiment at a time, stop at the decision point, and report before the next one. Never chain untested steps into a single run — a failure in the middle then has no clear cause.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.
