# Verify a bug bounty report contact before sending

## Verify the contact from the official source

- Read the reporting contact from the program official page or official docs before the first send to that program.

- Use the exact address or form the official source names, and do not reuse an address from an earlier draft or an earlier report without rechecking it.

- Record the official source and the address you verified beside the draft, so a later resend can recheck it.

- Stop and ask the user when the official source names no email address and no form, and do not guess an address from a common pattern.

- Treat a contact copied from a third party page or a chat message as unverified until the official source confirms it.

## Check for bounces and delivery after sending

- Treat a message in Sent as proof it left the mailbox only, and never as proof the recipient received it.

- Search the inbox for a bounce or delivery failure for that report after sending, and record the result beside the report including when no bounce appeared.

- When a bounce says the address does not exist, mark that address dead and never send another report to it.

- Before any later send to the same program, search for bounces on earlier sends to that program first, and reverify the address from the official source when an earlier send bounced.

## Resend to the corrected contact

- Find the corrected address from the official source, and verify it by reading the official text that names it.

- Read the original message from Sent before resending, and send the same report text to the corrected address.

- Verify the resend in Sent by reading back the recipient, and check for a new bounce after the resend.

- Tell the user at once when a report bounced, and name the corrected address and the resend plan.

## Available connectors

- [Gmail](/opt/hatch/connectors/gmail/CONNECTOR.md) for searching for bounces and sending the report.

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- When the program offers a form or a platform submission, use that route instead of email so delivery does not depend on an address.

- When the official source lists more than one contact, use the one it names for security reports and record why you chose it.
