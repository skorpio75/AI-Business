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

## ADR-004: Single-approver governance is MVP-only
- Status: Accepted
- Date: 2026-03-13
- Decision: The current single-CEO approval model remains valid for MVP, but it is not the long-term authorization model.
- Rationale: Production use beyond one operator requires role-based approval logic, delegation, separation of duties, and workflow-specific approval policy. This is now an explicit future direction.

## ADR-005: Policy enforcement will be separated from workflow code
- Status: Proposed
- Date: 2026-03-13
- Decision: Approval and outbound-action policy must evolve toward an explicit policy layer rather than remain embedded only in workflow code.
- Rationale: The platform will need workflow-specific approval rules, risk-based approval classes, and prevention of sensitive actions outside policy.

## ADR-006: LangGraph remains the workflow logic layer
- Status: Accepted
- Date: 2026-03-13
- Decision: LangGraph remains the primary orchestration layer for agent logic and workflow composition.
- Rationale: Existing workflows already depend on it, and there is no current justification to replace it.

## ADR-007: PostgreSQL remains the primary operational datastore
- Status: Accepted
- Date: 2026-03-13
- Decision: PostgreSQL remains the main operational store, with pgvector retained for semantic retrieval.
- Rationale: The next platform stage requires stronger schema discipline, not a second operational database.

## ADR-008: Production observability must extend beyond Langfuse
- Status: Proposed
- Date: 2026-03-13
- Decision: Langfuse is necessary but not sufficient; production observability must include structured logs, metrics, connector health visibility, routing visibility, and alerting.
- Rationale: The readiness assessment identifies silent or opaque failure modes as a major operational gap.

## ADR-009: Input and output safety controls are first-class platform requirements
- Status: Proposed
- Date: 2026-03-13
- Decision: Prompt-injection resistance, outbound content validation, attachment/document validation, and risky-output review gates must become explicit platform controls.
- Rationale: External business communication cannot rely only on operator intuition.

## ADR-010: Data lifecycle controls must be defined before broader production rollout
- Status: Proposed
- Date: 2026-03-13
- Decision: Retention, archival, deletion, backup, restore, and residency assumptions must be explicitly documented and implemented.
- Rationale: The platform handles email, documents, and business records, so lifecycle governance is mandatory.

## ADR-011: Client isolation must be operationally enforced, not only architecturally described
- Status: Accepted
- Date: 2026-03-13
- Decision: Track B must enforce tenant isolation at bootstrap, configuration, secrets, storage, and operations level.
- Rationale: Isolated deployment is already a core principle, but the assessment shows the operational enforcement is still incomplete.

## ADR-012: Mission Control will standardize on shadcn/ui
- Status: Accepted
- Date: 2026-03-13
- Decision: The React mission-control frontend will use `shadcn/ui` plus Tailwind as the default component foundation for operator-facing UI.
- Rationale: The current frontend has no established component system yet, and the next UI phase needs a consistent foundation before additional panels and cockpit views are added.

## ADR-013: Markdown governance files must remain aligned with roadmap status
- Status: Accepted
- Date: 2026-03-13
- Decision: `ROADMAP.md` is the implementation status source of truth, `TODO.md` is the short execution view derived from it, and any change to architecture, workflow scope, implementation status, integrations, or priorities must update all affected markdown governance files in the same work session.
- Rationale: The platform is managed markdown-first, so stale or conflicting docs create avoidable execution mistakes. Alignment must be treated as part of the change itself, not follow-up cleanup.

## ADR-014: The platform adopts a pod-based operating model
- Status: Accepted
- Date: 2026-03-14
- Decision: The operating model is formalized into Growth, Delivery, Ops, and Executive pods.
- Rationale: The repo already had strong workflow and specialist-agent coverage, but the handoff integration showed it needed clearer ownership boundaries and a reusable operating structure.

## ADR-015: Specialist agents are preserved as overlays in the pod model
- Status: Accepted
- Date: 2026-03-14
- Decision: Existing specialist roles such as CFO, Accountant, CTO/CIO, Chief AI / Digital Strategy, Compliance/Contract, and Procurement remain valid and are mapped into the pod model as overlays or adjacent specialists rather than being removed.
- Rationale: The repository's business ambition already depends on these specialist roles, and the pod model is intended to add structure, not flatten the agent taxonomy.

## ADR-016: Agent reuse is modeled as family, mode, and instance
- Status: Accepted
- Date: 2026-03-14
- Decision: Reusable capability is defined at the agent family level, while internal-operating and client-delivery use run as separate mode-specific instances with isolated memory, tools, and state.
- Rationale: This preserves reuse without breaking Track A and Track B isolation or accidentally sharing runtime state between internal operations and client work.

## ADR-017: State and event normalization are first-class platform contracts
- Status: Accepted
- Date: 2026-03-14
- Decision: `opportunity_state`, `project_state`, `run_state`, and `approval_state`, along with normalized event families and triggers, become formal architecture contracts.
- Rationale: The platform already persisted workflow state, but it lacked a clear cross-workflow operating language for handoffs, supervision, and future registry/runtime alignment.

## ADR-018: Tool access is governed through normalized tool IDs and permission profiles
- Status: Accepted
- Date: 2026-03-14
- Decision: Tool access is expressed through normalized IDs and policy-bound profiles rather than by ad hoc connector-specific capability assumptions.
- Rationale: Approval enforcement, auditability, and safe reuse across internal and client-delivery contexts require a consistent tool vocabulary.

## ADR-019: Autonomy classes distinguish advisory, execution, and approval-gated behavior
- Status: Accepted
- Date: 2026-03-14
- Decision: Agent autonomy is modeled through explicit classes such as `assistant`, `supervised_executor`, `bounded_autonomous`, and `approval_gated`.
- Rationale: The handoff integration identified autonomy boundaries as a missing control layer between workflow design, tool use, and approval policy.

## ADR-020: Mission Control is both UI and operating supervisor
- Status: Accepted
- Date: 2026-03-14
- Decision: Mission Control is not only a frontend shell; it is the platform's operating supervision layer for visibility, escalation, approval routing, and run-state observation.
- Rationale: The handoff integration clarifies that oversight is a first-class platform concern distinct from reasoning and workflow execution.
