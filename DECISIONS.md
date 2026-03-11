# Decisions

## Purpose
Architecture and implementation decisions with rationale and trade-offs.

## ADR-001: Isolated deployments per client
- Status: Accepted
- Date: 2026-03-09
- Decision: Each client runs an isolated instance (DB, data, credentials, logs).
- Rationale: Privacy, compliance, and operational clarity.

## ADR-002: Markdown-first project governance
- Status: Accepted
- Date: 2026-03-09
- Decision: All planning and agent/workflow specs are maintained in markdown.
- Rationale: Transparency, traceability, and low tooling overhead.

## ADR-003: Human approval for sensitive actions
- Status: Accepted
- Date: 2026-03-09
- Decision: No autonomous external action without approval in MVP.
- Rationale: Safety and trust during early operations.
