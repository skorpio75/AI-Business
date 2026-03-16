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

## ADR-021: PMO control and project-management execution coordination are distinct agent families
- Status: Accepted
- Date: 2026-03-14
- Decision: `PMO / Project Control Agent` is the governance, control-tower, steering, and portfolio-visibility role, while `Project Management / Delivery Coordination Agent` is the execution-follow-up role that keeps plans, tasks, checkpoints, and next actions moving.
- Rationale: The delivery model needs a stable distinction between governance oversight and day-to-day execution coordination, especially when the same firm operates both internal missions and client-delivery engagements.

## ADR-022: Multi-agent runtime evolution remains workflow-first and phased
- Status: Accepted
- Date: 2026-03-15
- Decision: The platform may evolve toward multi-agent pod runtimes, but the immediate path remains workflow-first. Runtime agents should first gain explicit step identity, handoff payloads, shared state contracts, execution logs, and step-level approval metadata before richer multi-agent routing is introduced.
- Rationale: The current architecture already has workflows, registry, approvals, and state foundations. A phased approach captures the value of multi-agent execution without prematurely adding autonomous peer orchestration, hidden complexity, or weakly observable routing behavior.

## ADR-023: A2A handoff is structured and workflow-mediated
- Status: Accepted
- Date: 2026-03-15
- Decision: The platform may use orchestrator/supervisor agents and specialized agents, but any agent-to-agent interaction must be structured through workflow-mediated handoffs, shared-state contracts, standardized payloads, and approval-policy enforcement.
- Rationale: This preserves the benefits of multi-agent specialization while avoiding an uncontrolled peer-agent mesh that would conflict with the workflow-first, approval-bound architecture.

## ADR-024: Reusable agent families may support billable client delivery through isolated instances
- Status: Accepted
- Date: 2026-03-15
- Decision: Agent families such as PMO, BA, Architect, Build, QA, Documentation, Knowledge, Reporting, Document, CTO/CIO, and Chief AI / Digital Strategy may be used both for internal company operations and for billable client delivery work, but only through separate client-scoped instances with isolated state, memory, tools, approvals, and audit history.
- Rationale: The business model depends on reusing proven agent capability across internal operations and client engagements without violating tenant boundaries or mixing Track 1 operating context with Track 2/client-delivery execution. This supports a commercial model where the firm bills for service outcomes produced with agent assistance rather than exposing or sharing internal runtime agents.

## ADR-025: Prompting is a dedicated runtime layer separate from the agent catalog
- Status: Accepted
- Date: 2026-03-15
- Decision: The target operating model will include a dedicated prompt layer composed of family-level base prompts plus workflow-step prompts, with runtime context injection for state, tools, approvals, tenant, and output schema. `AGENTS.md` remains the operating catalog for roles and boundaries rather than the primary location for prompt text.
- Rationale: Modular prompt composition is safer and more reusable than embedding one large prompt per agent in the business catalog. This approach fits the workflow-first architecture, reduces duplication across steps, and allows prompt authoring, versioning, evaluation, and rollback to evolve as a controlled runtime concern after contracts and workflow boundaries are stable.

## ADR-026: Prompt assets follow canonical naming, storage, and loading conventions
- Status: Accepted
- Date: 2026-03-15
- Decision: Prompt assets will follow canonical ID patterns and target filesystem conventions: family base prompts belong under `prompts/agents/<family_id>/system.txt`, workflow-step prompts belong under `prompts/workflows/<workflow_id>/<step_id_snake_case>.txt`, and the loader resolves explicit `relative_path` overrides first so existing legacy prompt files remain valid during migration.
- Rationale: The runtime prompt layer needs stable naming and storage rules so new prompt assets can be added consistently without requiring an immediate rewrite of every existing prompt file. Supporting explicit-path compatibility keeps the current MVP prompt set working while we gradually migrate toward the cleaner canonical layout.

## ADR-027: Client-facing advisory agents must analyze explicit client briefs before recommending services
- Status: Accepted
- Date: 2026-03-15
- Decision: Client-facing advisory families such as `CTO/CIO Agent` and `Chief AI / Digital Strategy Agent` must accept a bounded client brief that includes a problem statement plus relevant client context/history, constraints, and desired outcomes, and they must generate recommendations from that brief rather than from generic static packaging alone.
- Rationale: Advisory value depends on interpreting the client's real situation, not only exposing a reusable internal offer catalog. A typed client-brief contract preserves Track A/Track B isolation while allowing specialist agents to deliver credible consulting, counseling, and AI strategy outputs grounded in the engagement context.

## ADR-028: Client-facing advisory agents should behave like consulting agents, not only analyzers
- Status: Accepted
- Date: 2026-03-15
- Decision: Client-facing advisory agents should frame the active consulting mission, recommend the best-fit initial service, and detect bounded upsell or follow-on opportunities that can responsibly grow the client account, while staying grounded in the same client brief and tenant boundaries.
- Rationale: A consulting company grows by solving the current mission well and by noticing adjacent opportunities that are genuinely relevant to the client. Making this posture explicit in the agent contract helps the platform support real consulting behavior instead of stopping at one-off problem analysis.

## ADR-029: Specialist consulting and counseling should use the shared LLM runtime with governed fallback
- Status: Accepted
- Date: 2026-03-15
- Decision: Specialist consulting and counseling surfaces such as the `CTO/CIO Agent` and `Chief AI / Digital Strategy Agent` should perform their primary reasoning through the shared prompt/model layer and `ModelGateway`, while deterministic logic remains as a fallback for resilience, output-shape recovery, and governance guardrails.
- Rationale: High-value consulting, internal counseling, and client-facing deliverables depend on LLM reasoning capacity and cannot be reduced to static keyword heuristics alone. Keeping that reasoning inside the governed prompt/model layer preserves routing visibility, prompt controls, output schemas, and future auditability.

## ADR-030: Heavy internal specialist panels should be section-assembled with configurable model timeouts
- Status: Accepted
- Date: 2026-03-16
- Decision: The internal CTO/CIO and Chief AI specialist panels should assemble their responses from multiple smaller section-level prompt/model calls instead of one oversized structured generation, the shared model timeout should be configurable through runtime settings and `.env`, and the heavy internal panel sections should favor compact line-oriented prompts plus a fast local-model override over large structured JSON generations.
- Rationale: Direct end-to-end panel generation can exceed local Ollama latency budgets for complex advisory outputs, especially on smaller local models. Splitting the work into narrower calls improves the chance of local completion while preserving governed fallback, making the timeout configurable avoids hard-coding one latency budget for every environment, and compact example-shaped prompts keep the local path reliable without reverting the panels to deterministic-only outputs.

## ADR-031: Agent-family LLM routing should be governed by a separate routing matrix
- Status: Accepted
- Date: 2026-03-16
- Decision: The platform should maintain a separate agent-family LLM routing matrix that distinguishes compact direct-Ollama local-first execution, compact local drafting with stronger guardrails, richer governed `ModelGateway` reasoning, and deterministic/tool-first hybrids. This routing posture should be planned by family and mode rather than assuming one LLM execution pattern fits every agent.
- Rationale: The agent catalog includes internal panels, grounded knowledge services, operational control roles, client-delivery authoring roles, and richer client-facing consulting surfaces. Those families do not share the same latency, structure, risk, or review needs. A dedicated routing matrix keeps LLM adoption explicit, auditable, and aligned with governance without forcing all families into the same local or cloud pattern.

## ADR-032: Track B bootstrap should start from a reusable client template pack
- Status: Accepted
- Date: 2026-03-16
- Decision: The first Track B bootstrap layer should be represented as a reusable client template pack under `config/client-template/` that bundles a starter client config, a client-scoped environment template, a compose overlay, and a canonical storage/secret path map before later work adds fuller client contracts, seed automation, and enforced runtime isolation.
- Rationale: Track B needs a concrete cloneable starting point before deeper bootstrap automation exists. Packaging these artifacts together creates an explicit handoff surface for later seeding and isolation work while preserving the architectural rule that Track A and Track B reuse the same codebase but not the same tenant, storage, or credential assumptions.

## ADR-033: The Track B client template contract must carry bootstrap-critical runtime defaults
- Status: Accepted
- Date: 2026-03-16
- Decision: `config/client-template/client.yaml` should define the canonical Track B client contract for tenant identity, governance defaults, deployment metadata, storage and secret paths, connector defaults, model-routing posture, and initial workflow/service packaging so later seed automation can treat one file as the source of truth for a new client instance.
- Rationale: The template pack is only partly useful if the key bootstrap assumptions remain scattered across docs or implied by other config files. A fuller client contract improves repeatability, keeps Track B bootstrap deterministic, and gives later seeding and isolation work one governed handoff artifact instead of several disconnected placeholders.

## ADR-034: Track B runtime must enforce tenant-scoped env, secret, and storage boundaries
- Status: Accepted
- Date: 2026-03-16
- Decision: Track B runtime settings must reject client instances that fall back to the shared root `.env` or that point storage, prompt-override, or connector-secret paths outside the tenant-scoped roots defined for that client. Provider token persistence should follow the active client env file, and startup should create the validated tenant-scoped runtime directories before connector bootstrap runs.
- Rationale: Track B isolation is not credible if credentials can still drift into the shared repo `.env` or if client storage paths can point at shared roots. Runtime validation and path-aware token persistence close the gap between the template contract and actual operational behavior.

## ADR-035: Track B bootstrap should emit tenant-specific generated config outside the shared template pack
- Status: Accepted
- Date: 2026-03-16
- Decision: The client initialization seed flow should treat `config/client-template/` as the shared source template and write generated per-client artifacts into `config/clients/`, including a tenant-specific client contract and runtime env file, while also creating the tenant directory roots required by runtime isolation.
- Rationale: Keeping generated client artifacts separate from the reusable template pack preserves the distinction between shared blueprint assets and tenant-specific operational config. It also makes repeated seeding safer and clearer, especially once multiple Track B client instances exist side by side.

## ADR-036: Track B portability validation must distinguish runnable services from contract-only workflow pack entries
- Status: Accepted
- Date: 2026-03-16
- Decision: Track B portability acceptance should prove that implemented reusable workflows run across multiple seeded client instances under tenant-scoped runtime settings, while separately verifying that additional workflow-pack entries remain preserved in the seeded client contract and shared workflow registry until their service implementations land.
- Rationale: This keeps portability claims honest. The platform should not imply full end-to-end portability for workflows that are only documented in the client pack today, but it should still protect the shared Track B contract so later implementations can plug into an already-stable workflow pack.
