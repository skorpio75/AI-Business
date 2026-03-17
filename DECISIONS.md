<!-- Copyright (c) Dario Pizzolante -->
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

## ADR-037: Mission Control should expose governed agent operating-model metadata
- Status: Accepted
- Date: 2026-03-16
- Decision: Agent Activity and similar operator-facing Mission Control views should describe each agent through governed metadata, including pod/family/mode context plus a readable runtime posture label such as direct `Ollama`, governed `LiteLLM`/`ModelGateway`, or descriptive/tool-first execution.
- Rationale: Operator trust depends on seeing more than a friendly agent name. Surfacing the operating model directly in Mission Control makes routing posture legible, reduces UI copy drift from backend/runtime reality, and gives the CEO a faster way to understand what kind of agent behavior is being invoked.

## ADR-038: Microsoft To Do task activation should reuse the same Graph tenant/client context and remain approval-bound
- Status: Accepted
- Date: 2026-03-16
- Decision: When the personal assistant expands from inbox/calendar into Microsoft To Do, it should use the same Microsoft Graph tenant, client ID, and operator account context as Outlook mail/calendar for that instance. Assistant recommendations may become candidate tasks, but task creation and approved priority assignment must remain explicit approval-bound writes with audit visibility.
- Rationale: Reusing one Graph app boundary keeps provider identity and tenant scoping simple, avoids avoidable connector sprawl, and turns recommendations into actionable tasks without weakening the platform's approval-first governance model.

## ADR-039: Track B bootstrap must be documented as an operator runbook centered on tenant env activation
- Status: Accepted
- Date: 2026-03-16
- Decision: Track B should ship with a concrete bootstrap runbook that documents the exact seed, startup, connector-bootstrap, verification, and cleanup sequence, with explicit emphasis that `RUNTIME_ENV_FILE` must be set before any Python process starts for a client instance.
- Rationale: Isolation is enforced partly by runtime configuration selection, not only by static files. A generated tenant env file is not enough if operators can still launch migrations, the API, or token bootstrap scripts against the shared root `.env`. A runbook turns the bootstrap path into a repeatable operational procedure instead of relying on implicit knowledge.

## ADR-040: Langfuse tracing should be optional and attached at workflow and model-gateway seams
- Status: Accepted
- Date: 2026-03-16
- Decision: Langfuse integration should be env-gated and fail-open, with workflow/service spans added at the reusable workflow entry points and nested generation observations added inside the shared `ModelGateway` for local, cloud, and fallback routing paths.
- Rationale: Observability needs to illuminate real routing and workflow behavior without becoming a new source of runtime fragility. Instrumenting the shared gateway plus current workflow entry points captures high-value traces for prompts, provider/model selection, and fallback behavior while preserving MVP resilience when Langfuse is not configured.

## ADR-041: Unit tests should share a lightweight base layer instead of repeating setup inline
- Status: Accepted
- Date: 2026-03-16
- Decision: The unit test suite should standardize common setup through a small shared base layer in `tests/unit/base.py`, covering repo-root lookup, settings construction without env-file loading, temporary directories, in-memory SQLite sessions, and Track B seeded-client lifecycle helpers.
- Rationale: The suite was already repeating the same setup patterns across tests, especially for Track B env switching and ephemeral DB setup. A lightweight base layer reduces duplication and makes later Phase 5 work easier without prematurely introducing a heavy fixture framework before reuse patterns are stable.

## ADR-042: API integration tests should exercise FastAPI through an in-process client with dependency overrides
- Status: Accepted
- Date: 2026-03-16
- Decision: API integration coverage should run against the real FastAPI app via an in-process `TestClient`, using dependency overrides for database sessions and targeted patching for global service singletons or startup/bootstrap seams when external dependencies would otherwise make the route non-deterministic.
- Rationale: The goal of API integration tests is to validate routing, request/response schemas, dependency injection, serialization, and persistence behavior without requiring external infrastructure for every test run. An in-process client keeps the coverage close to real HTTP behavior while preserving speed and determinism for the local suite.

## ADR-043: Workflow branch tests should explicitly cover approval and escalation behavior
- Status: Accepted
- Date: 2026-03-16
- Decision: The workflow-test layer should cover approval decision branches through HTTP-level tests and escalation/routing branches through focused service-level tests, with these scenarios organized under `tests/workflow/`.
- Rationale: Approval and escalation regressions are too workflow-specific to fit cleanly inside generic unit tests, but they do not always require a full external integration environment. A dedicated workflow-test layer keeps these branches visible and targeted, especially for `email-operations`, where routing, fallback, and approval outcomes all materially affect operator trust.

## ADR-044: Repeated test payloads should use lightweight shared builders
- Status: Accepted
- Date: 2026-03-16
- Decision: Repeated test request bodies, connector-status responses, and Track B runtime settings should be centralized in a lightweight builder module under `tests/sample_data.py` rather than duplicated inline across unit, integration, and workflow tests.
- Rationale: By Phase 5, the suite had recurring email workflow payloads, approval decisions, connector bootstrap responses, and tenant-scoped settings shapes spread across multiple test layers. Small shared builders reduce drift and maintenance cost while preserving the repo's current lightweight `unittest` style without introducing a heavier fixture framework prematurely.

## ADR-045: Auditability should use a first-class platform audit model
- Status: Accepted
- Date: 2026-03-16
- Decision: The platform should define a dedicated audit model in `AUDIT_MODEL.md` with canonical `agent_run` and `audit_event` objects, normalized audit event families, and explicit linkage to workflow runs, approvals, tool IDs, autonomy classes, approval classes, and external observability traces.
- Rationale: Traceability requirements are already spread across workflows, approvals, Mission Control, Langfuse spans, and later roadmap items such as `agent_runs`, `audit_events`, and audit endpoints. A first-class audit model gives those future persistence and UI surfaces one governed contract instead of letting each implementation invent its own trace vocabulary.

## ADR-046: Hybrid RAG should separate grounded internal or client evidence from external enrichment
- Status: Accepted
- Date: 2026-03-16
- Decision: The platform should evolve toward a hybrid retrieval model where shared workspace plus internal and tenant-scoped client corpora provide primary grounding, while external web retrieval broadens context as a cited enrichment layer rather than silently becoming authoritative business truth.
- Rationale: Internal operations and client-facing consulting both benefit from broader context, but the platform's governance model depends on preserving clear provenance and keeping current state authoritative only when written through approved workflows. Separating grounded evidence from external enrichment improves trust, auditability, and safer consulting outputs.

## ADR-047: Judge or controller behavior in multi-agent flows should be a bounded review or gate step
- Status: Accepted
- Date: 2026-03-16
- Decision: Review or judge-style agents such as `QA / Review Agent`, `Risk / Watchdog Agent`, or `Mission Control Agent` may be used in multi-agent workflows only as explicit rubric-driven steps that return finite outcomes such as `approve`, `revise`, `escalate`, or `human_review`.
- Rationale: A bounded review or gate step adds real value for high-impact consulting, proposal, and delivery outputs, especially when hybrid retrieval is involved. But making every task pass through a universal autonomous judge would add cost, latency, and opaque control flow that conflicts with the workflow-first architecture.

## ADR-048: Client-facing consultant agents are instantiated per client, engagement, and mission
- Status: Accepted
- Date: 2026-03-16
- Decision: Reusable consulting families such as `CTO/CIO Agent`, `Chief AI / Digital Strategy Agent`, `PMO / Project Control Agent`, `Architect Agent`, and related delivery-support families should run as mission-bound instances keyed to a specific `tenant`, `client`, `engagement`, and `mission`, rather than as one generic client-facing consultant runtime shared across accounts.
- Rationale: The business model depends on reusing capability without sharing runtime identity or context across clients. Mission-bound instantiation preserves tenant isolation, keeps RAG and working memory scoped to one client context, and makes portfolio-level visibility legible because each dispatched consultant can be traced back to a concrete engagement and objective.

## ADR-049: Track A portfolio visibility must aggregate bounded client-runtime summaries rather than shared mutable client state
- Status: Accepted
- Date: 2026-03-16
- Decision: Track A Mission Control should evolve into a portfolio cockpit that can show clients, engagements, missions, dispatched consultant-agent counts, active runs, approvals, and risk across the client portfolio, but it must do so through bounded telemetry or summary feeds from isolated client runtimes rather than by centralizing client-local mutable state in one shared control plane.
- Rationale: The CEO needs a genuine fleet view over consultant-agent deployment and health. But the core architecture and Track B isolation rules would be weakened if Track A became the writeable source of truth for all client delivery state. Summary-based portfolio visibility preserves both executive oversight and tenant isolation.

## ADR-050: Lead spotting and materialization happen in Track A before normal Growth workflows begin
- Status: Accepted
- Date: 2026-03-16
- Decision: The platform should distinguish raw `lead_signal` inputs from materialized leads. Supported source classes may include manual entry, inbound email, website forms, calendar bookings, referrals, CRM imports, document intake, chat, and researched account signals. Automatic lead creation is allowed only when source identity, account or contact context, and a consulting need are sufficiently clear; otherwise the signal should become a reviewable candidate rather than silently entering the active pipeline.
- Rationale: The current Growth flow already assumes `lead.received`, but real commercial intake starts earlier and is often noisy. A governed Track A materialization layer keeps the sales process realistic, preserves auditability, supports automation for non-manual sources, and prevents low-quality external signals from polluting `opportunity_state`.

## ADR-051: Signed scope must produce an approved dispatch plan before mission startup
- Status: Accepted
- Date: 2026-03-16
- Decision: A signed contract or accepted SOW should not activate client delivery directly. The platform should first produce a `dispatch_candidate_plan` that proposes the consultant swarm, deliverables, assumptions, tool boundaries, and budget implications for the mission. CEO approval of that plan should materialize an `approved_consultant_roster`, which then becomes the basis for Track B mission-bound instance activation and Mission Control portfolio visibility.
- Rationale: Real consulting delivery normally includes a staffing and startup decision between commercial agreement and execution. Making that step explicit improves scope control, budgeting, delivery readiness, and visibility over which consultant agents are actually dispatched to each client mission.

## ADR-052: Milestone billing remains an internal Track A control driven by client-approved delivery evidence
- Status: Accepted
- Date: 2026-03-16
- Decision: Track B delivery instances may prepare milestone evidence and acceptance packets, but invoice triggering, release, receivables follow-up, and closeout billing control remain internal Track A responsibilities governed by an approved `billing_plan`. Billing should begin from client-approved milestone acceptance or other approved billing conditions rather than from internal delivery completion alone.
- Rationale: This preserves the commercial reality of consulting work: delivery evidence is client-scoped, but billing authority and cash collection remain internal firm responsibilities. Separating milestone completion from client acceptance and invoice release improves auditability and avoids accidental billing drift.

## ADR-053: Delivery quality gates should be mission-specific, phase-aware, and agent-run
- Status: Accepted
- Date: 2026-03-16
- Decision: Delivery quality control should not be modeled as one generic QA step at the end of execution. Each mission should carry a `quality_gate_plan` derived from the SOW, project plan, deliverable classes, and acceptance criteria, with checkpoints that can review documents, architecture, code, automation outputs, test evidence, milestone readiness, and handoff completeness. These gates should be executed by bounded review families such as `QA / Review Agent`, `Testing / QA Agent`, `Documentation Agent`, and when justified `Risk / Watchdog Agent`.
- Rationale: Real consulting work applies different quality checks at different delivery phases. A mission-scoped, AI-assisted gate model better reflects how planning, implementation, milestone release, and handoff are actually governed, while keeping review behavior observable and workflow-bound instead of ad hoc.

## ADR-054: Internal and client-scoped agent modes are chosen by business purpose, not by family alone
- Status: Accepted
- Date: 2026-03-16
- Decision: Reusable families may exist in `internal_operating`, `client_delivery`, or `client_facing_service` mode, but the selected mode must follow the business process being served. Track A `internal_operating` instances are used for the firm's own lead, proposal, approval, dispatch, billing, and portfolio-control processes. Track B `client_delivery` instances are used for tenant-scoped mission execution. `client_facing_service` instances remain separate client runtimes for bounded advisory or service outputs and must not be treated as the same runtime identity as the internal agent.
- Rationale: Without an explicit usage rule, the platform risks blurring pre-sales/internal control work with client mission execution. Tying mode selection to business purpose preserves isolation, clarifies when Track B should start, and makes the lifecycle easier to operate and audit.

## ADR-055: `agent_runs` should land as the first persisted audit primitive before step-level `audit_events`
- Status: Accepted
- Date: 2026-03-16
- Decision: The platform should persist bounded `agent_runs` first, using a summary table linked to tenant, track, agent family, mode, workflow IDs where available, and provider or model metadata across the current workflow and specialist-advisory seams before introducing the more granular append-oriented `audit_events` layer.
- Rationale: Existing traceability was split across workflow runs, snapshots, approvals, and optional Langfuse spans. Adding `agent_runs` first creates one durable execution-history backbone for Mission Control and later audit work without forcing the repo to define every step-level event and tool-action contract in the same slice.

## ADR-056: `audit_events` should append normalized step, tool, approval, and outbound-action history onto `agent_runs`
- Status: Accepted
- Date: 2026-03-16
- Decision: The platform should persist append-oriented `audit_events` next, linked to `agent_runs` where possible, and use them for normalized workflow-step outcomes, model-route choices, tool-call history, approval lifecycle events, and outbound email-send actions across the current implemented seams.
- Rationale: `agent_runs` answer which bounded execution happened, but they do not provide the timeline needed to inspect approval handling, step transitions, or connector actions. A dedicated `audit_events` table preserves those details in one normalized event stream without overloading the summary role of `agent_runs`.

## ADR-057: Audit inspection should expose aggregated workflow, approval, and agent trace views before richer Mission Control UI work
- Status: Accepted
- Date: 2026-03-16
- Decision: The first read surface for auditability should be a small set of aggregated API endpoints that return bundled workflow, approval, and agent traces over persisted `workflow_runs`, approvals, `agent_runs`, and `audit_events` rather than exposing only low-level raw-table endpoints.
- Rationale: Operators and the later UI need coherent inspection shapes immediately, but the Mission Control presentation work still comes later. Aggregated trace endpoints make the audit layer usable now while keeping room for stricter normalization and richer frontend views in subsequent tasks.

## ADR-058: Track A should support an internal delivery-lab lane for delivery-family dogfooding and rehearsal
- Status: Accepted
- Date: 2026-03-17
- Decision: Track A `internal_operating` mode should support bounded delivery-family invocation through `ad_hoc_session`, `saved_lab_mission`, and engagement-bound internal runs so the firm can use and test delivery capabilities before a real client runtime exists.
- Rationale: If delivery families can only run after a real client mission starts, the platform delays learning, reduces dogfooding value, and makes Track B the first real proving ground. A governed Track A delivery-lab lane improves rehearsal, artifact preparation, operator familiarity, and prompt or workflow hardening without weakening the Track B isolation model.

## ADR-059: Promotion from Track A rehearsal into Track B must use explicit handover and readiness artifacts
- Status: Accepted
- Date: 2026-03-17
- Decision: Promotion from Track A internal rehearsal into Track B must happen through a bounded `handover_pack`, `readiness_gate_result`, and `activation_request`, rather than by sharing mutable Track A runtime state, memory, or agent identity directly into the client runtime.
- Rationale: Track A should be able to prepare and validate delivery work, but Track B must remain the authoritative tenant-scoped execution plane. Explicit promotion artifacts preserve auditability, improve readiness review, and prevent accidental coupling between internal rehearsal state and live client delivery state.

## ADR-060: Cloud deployment should evolve from Track A-first rollout to later Track B scale-out with separate inference lanes
- Status: Accepted
- Date: 2026-03-17
- Decision: Production deployment should start with a Track A-first subscription and later add Track B runtimes only when client demand exists. Track A may use its own internal `Ollama` path, Track B may later use a shared `Ollama` inference service to reduce hosting duplication, and governed cloud fallback must remain available through the shared model gateway and routing matrix.
- Rationale: The platform should not force full Track B infrastructure cost before there are real client missions. A staged rollout reduces cost and operational burden early, while separate internal and client inference lanes preserve clearer ownership, better local iteration for Track A, and cleaner options for later client-scale hosting.
