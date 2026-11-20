# Alert the user at once on a validated bug bounty finding

## Define what counts as validated

- Treat a finding as validated only when you have a reproduction or proof of concept, a severity, the affected program, and the impact in plain words.

- Treat a lead, a single unreproduced observation, or a case that still needs a proof of concept as unvalidated and keep it out of the immediate alert path.

- Read the current scope from the user latest order before each wave, because the scope has changed between Critical only and Critical plus High, and do not hardcode one scope.

## Make the coordinator return at once

- Instruct every hunt coordinator to finish its turn and return the moment it validates a Critical or High finding, instead of finishing the wave first.

- Tell the coordinator to send the validation timestamp, the program, the severity, the impact, the evidence location, and any submission blocker in that return, and to hold nothing for a batch summary.

- Treat a coordinator return that carries a validated Critical or High finding as an interrupt, not as a wave summary to file away.

## Message the user before anything else

- Send a message to the user in the main chat as soon as you receive a validated Critical or High finding, before starting any other work.

- State the severity, the program, the impact, the reward range when known, and the next step that needs the user, in that message.

- Never hold a validated Critical or High finding for a status check, a wave summary, or a reply to a user question, and never let the user discover it only by asking what is valid.

- Record the validation timestamp and the notification timestamp beside the finding in the valid findings archive, so the delay stays auditable.

## Keep hunting after the alert

- Relaunch the next hunt wave after sending the alert, and keep hunting even when the user has not replied or submitted yet.

- Route Medium and lower findings, report only cases, and unvalidated leads to the archive and the next batch summary, and keep them out of the immediate alert path.

- When a submission is blocked, say the blocker and the unlock path in the alert message, and do not treat the block as a reason to delay the alert.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- When no new Critical or High finding appears, send nothing extra and let the hunt continue quietly, so the alert keeps its meaning.

- When several findings validate at once, send one message per finding in severity order, so no Critical finding hides behind a High one.