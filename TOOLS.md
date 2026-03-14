# Tools

## Purpose
Define the normalized tool taxonomy and permissions model used by agents and workflows.

## Tool Model
- Tools are named by normalized IDs.
- Agents do not receive raw connector or implementation access by default.
- Policies decide whether a workflow step may invoke a tool.
- Sensitive tools require approval even when an agent family is otherwise allowed to request them.

## Tool Namespaces

### Communication
- `email.read`
- `email.draft`
- `email.send_internal`
- `email.send_external`
- `calendar.read`
- `calendar.write`
- `meetings.ingest_transcript`

### Commercial
- `crm.read`
- `crm.write`
- `contacts.read`
- `proposals.read_template`
- `pricing.read_rules`
- `pricing.run_estimate`
- `research.web_search`

### Delivery
- `pm.read`
- `pm.write`
- `tasks.read`
- `tasks.write`
- `docs.read`
- `docs.write`
- `repo.read`
- `repo.write`
- `code.run_sandbox`
- `workflow.deploy_nonprod`

### Operations
- `finance.read`
- `finance.write_draft`
- `invoices.generate_draft`
- `payments.read`
- `vendors.read`
- `vendors.write`
- `hr.read`
- `hr.write_limited`

### Core
- `memory.search`
- `memory.write`
- `state.read`
- `state.write`
- `approval.request`
- `reporting.generate`
- `audit.log`

## Permission Model
- Read tools retrieve data or context.
- Draft tools produce drafts or non-authoritative writes.
- Action tools create, send, deploy, or mutate authoritative state.

## Approval-Gated Tool Patterns
- `email.send_external`
- `calendar.write` for client-facing commitments
- `crm.write` when it commits externally relevant status
- `finance.write_draft` when it changes authoritative financial records
- `vendors.write`
- `repo.write` when used against controlled client or production repositories
- `workflow.deploy_nonprod`

## Mode-Specific Tool Boundaries
The same agent family may receive different tool profiles by mode.

Example:
- internal `PMO / Project Control Agent` may use `finance.read` and portfolio-level `pm.write`
- client-delivery `PMO / Project Control Agent` may use `pm.write`, `tasks.write`, and `docs.write`, but not company-level finance tools

## Deny-by-Default Rule
- New tools are denied by default until assigned to a profile or workflow.
- External connectors map to normalized tool IDs rather than bypassing policy.
