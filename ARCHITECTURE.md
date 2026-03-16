# Architecture

## 1. Top-Down View
The system is built as a reproducible enterprise agent platform blueprint with isolated deployments.

```text
Interfaces
  ->
Workflows
  ->
Prompt Layer
  ->
Agent Modules
  ->
Tools and Actions
  ->
Policies and Approvals
  ->
State and Events
  ->
Memory
  ->
Platform Foundation
  ->
Infrastructure
```

## 2. Deployment Model
### Shared
- codebase
- architecture
- workflow templates
- agent templates
- configuration schema
- deployment scripts

### Isolated per instance
- database
- vector index
- credentials
- documents
- logs
- company context
- connectors

## 3. Layer Breakdown
### Interfaces
- React operator console using `shadcn/ui` as the default component system for mission control surfaces
- FastAPI endpoints
- typed specialist advisory-analysis endpoints for client problem/context assessment
- consulting-oriented specialist analysis outputs that frame the active mission and adjacent account-growth opportunities
- LLM-backed specialist reasoning through the shared prompt/model layer, with deterministic fallback and schema guardrails
- operator-facing agent views should expose governed operating-model metadata, including whether a surface is direct `Ollama`, governed `LiteLLM`/`ModelGateway`, or descriptive/tool-first
- personal assistant operator views are planned to unify inbox, calendar, and Microsoft To Do context under one provider identity, with recommendation-to-task promotion remaining approval-bound before write-back

### Workflows
- LangGraph orchestration

### Prompt Layer
- family-level base prompts
- workflow-step prompts
- runtime prompt/template loader
- context injection for state, tool profile, approvals, tenant, and output schema
- typed prompt composition contracts and config bindings
- canonical prompt naming, storage, and loading conventions

### Agent Modules
- Python modules
- Pydantic contracts

### Tools and Actions
- provider connectors
- bounded external actions
- normalized tool IDs and tool profiles

### Policies and Approvals
- approval-first model for sensitive actions
- later role-based policy enforcement
- autonomy classes and approval classes

### State and Events
- normalized event families and workflow triggers
- canonical operating state objects
- run and approval state for Mission Control visibility

### Memory
- working memory
- episodic memory
- semantic memory

### Platform Foundation
- LiteLLM
- LlamaIndex
- PostgreSQL
- pgvector
- Langfuse (planned operational tracing in Phase 5)
- Jinja2
- Pydantic Settings

### Infrastructure
- Docker Compose
- PostgreSQL
- local file storage

## 4. MVP Workflow Coverage
### Implemented end-to-end in the current internal MVP
- email operations
- internal knowledge Q&A
- proposal generation

### Defined as workflow templates or next-stage operator surfaces
- document intake
- billing and collections
- finance reporting
- procurement (PO)
- project delivery control
- quality/testing gate
- documentation handover

## 5. Current Track A Delivery State
- Mission Control runs as a React operator console with a `shadcn/ui` + Tailwind component foundation in `frontend/`.
- Mission Control groups navigation by operating task and constrains detail panes so operator views remain readable across desktop and tablet layouts.
- Provider-backed Gmail, Google Calendar, and Microsoft Graph read connectors are available for live inbox/calendar context.
- Approved Outlook replies can execute through Microsoft Graph after approval is recorded in this platform.
- Mission Control exposes explicit routing visibility for local model, cloud route, fallback-rule execution, and whether the local LLM was invoked.
- Mission Control now includes CTO/CIO, finance, and Chief AI / Digital Strategy specialist panels backed by typed API summaries.
- CTO/CIO and Chief AI specialist APIs now also accept bounded client briefs so advisory instances can analyze problem statements, context/history, and recommend relevant services.
- Those specialist analysis contracts now also frame the client mission and surface bounded upsell opportunities for consulting-led account growth.
- CTO/CIO and Chief AI specialist analysis now runs through the shared model gateway and prompt layer, while deterministic logic remains as a governance-friendly fallback path.
- The internal CTO/CIO and Chief AI specialist panels now also run through the shared model gateway, expose routing metadata in Mission Control, and are assembled from smaller section-level model calls that use compact line-oriented prompts and a fast local-model override to reduce local-model timeout pressure.
- Shared model timeout control is environment-configurable through `MODEL_TIMEOUT_SECONDS` so local and cloud routing can be tuned without code edits.
- Agent-family routing posture is now documented separately in `AGENT_LLM_ROUTING_MATRIX.md` so compact direct-Ollama, guarded local drafting, richer governed gateway reasoning, and deterministic/tool-first hybrids are planned explicitly by family rather than assumed uniformly across the catalog.
- Provider bootstrap now supports Microsoft Graph device-code onboarding, Google local-loopback OAuth onboarding, refresh-token lifecycle handling, and optional JSON secret-store paths for Google and Microsoft connector credentials.
- Track B now has an initial deployment template pack in `config/client-template/` with a starter client config, client-scoped env template, compose overlay, and canonical storage/secret path map for cloned client instances.
- That Track B client config is now expanded into a fuller contract that captures tenant identity, approval/governance defaults, deployment metadata, storage and secret paths, connector defaults, model-routing posture, and initial workflow/service packaging for later bootstrap automation.
- `scripts/seed_config.py` now materializes tenant-specific client contracts and runtime env files under `config/clients/` and prepares the tenant-scoped storage, prompt, and secret roots expected by the runtime.
- Track B runtime settings now enforce tenant-scoped env, secret, storage, and prompt-root boundaries, and startup creates those tenant-scoped directories before connector bootstrap runs.
- Track B portability validation now proves that seeded client instances can run the reusable `knowledge-qna` and `email-operations` workflows under tenant-scoped settings, while `document-intake` and `reporting` remain governed workflow-pack contract entries until their service implementations exist.
- `docs/track-b-bootstrap-runbook.md` now captures the operator sequence for seeding, activating `RUNTIME_ENV_FILE`, starting tenant-scoped infrastructure, bootstrapping connectors, and verifying a client instance without falling back to shared Track A defaults.

## 6. Architectural Rule
The workflow controls the process. AI is used only inside selected steps.

## 7. Operating Model
- Single human CEO approval authority for high-risk actions.
- Agent modules are organized into a 4-pod operating model:
  - Growth
  - Delivery
  - Ops
  - Executive
- Existing specialist roles remain valid as overlays across pods rather than being removed.
- Agent reuse follows a `family -> mode -> instance` model.
- The same family may exist in internal-operating and client-delivery forms, but runtime instances, memory, tools, and state remain isolated.
- Mission Control is both the operator UI surface and the operating supervisor layer for visibility, escalation, approval routing, and audit.

## 8. Memory Model
- Working memory: active workflow state and approval checkpoints.
- Episodic memory: past runs, approvals, and traces.
- Semantic memory: retrieved knowledge from documents and vector search.
- Shared workspace: current operational truth for clients, projects, tasks, invoices, and related entities.

## 9. Formal Operating Layer
The handoff integration adds an explicit formal operating layer to the architecture:

- pod ownership for Growth, Delivery, Ops, and Executive work
- normalized events and triggers for workflow start and stage progression
- canonical state objects for opportunity, project, run, and approval state
- explicit ownership and persistence mapping for opportunity, project, run, and approval state in backend contracts/config
- normalized tool taxonomy and permissions
- reusable tool-permission profiles bound by agent family and operating mode
- autonomy classes that bound what agent instances may do
- a modular prompt model that separates family-level base prompts from workflow-step prompts
- typed prompt-layer contracts for prompt assets, composition rules, and injected operating context
- typed specialist advisory-analysis contracts for client briefs, context signals, and service recommendations
- consulting-oriented specialist contracts for mission framing and account-growth opportunity discovery
- specialist analysis responses now include provider/model routing metadata for traceability
- operator-facing agent descriptions should be able to map registry metadata and routing posture into a readable operating-model summary without inventing a separate UI-only taxonomy
- specialist overlay roles that complement, rather than replace, pod-native agents
- a delivery distinction between `PMO / Project Control Agent` as governance/control-tower role and `Project Management / Delivery Coordination Agent` as day-to-day execution-follow-up role

### Prompt Architecture Principle
Prompting is a first-class runtime layer in the target architecture, but it is not the same thing as the business agent catalog.

- `AGENTS.md` defines operating roles and runtime boundaries
- family-level base prompts define durable behavioral instructions for an agent family
- workflow-step prompts define task-specific instructions for a bounded execution step
- runtime execution composes base prompt, step prompt, and injected operating context rather than relying on one giant static agent prompt
- backend prompt contracts live in `app/models/prompt_layer.py`, mirrored in `config/base/prompt_layer.yaml`, and rendered through the composable loader in `app/core/prompt_loader.py`
- the target filesystem convention is `prompts/agents/<family_id>/system.txt` and `prompts/workflows/<workflow_id>/<step_id_snake_case>.txt`, while legacy explicit `relative_path` mappings remain valid during migration
- prompt expansion should be phased after state contracts, tool boundaries, approvals, and workflow choreography are stable enough to support safe reuse and evaluation

## 10. Multi-Agent Evolution Principle
The platform may evolve into richer multi-agent pod runtimes, but only under these constraints:

- workflows remain the top-level control model
- agents execute bounded steps rather than forming an autonomous peer mesh
- per-step `agent_id`, handoff payloads, shared state contracts, and approval-policy metadata exist before deeper dynamic routing is introduced
- Growth is the best first true multi-agent pod because it has a clear `opportunity_state` and natural bounded handoffs
- Delivery becomes the flagship multi-agent runtime only after the foundational execution contracts and observability controls are in place
- Executive and finance synthesis agents should depend on signals produced by mature Growth and Delivery runtimes rather than being promoted prematurely

### Orchestrator and Supervisor Model
The intended multi-agent runtime supports:

- workflows as the primary orchestrator
- specialized agents as bounded executors
- optional supervisor/orchestrator agents such as `Mission Control Agent` or later pod-specific supervisors

The architecture does not target unconstrained peer-agent autonomy. Supervisor behavior must remain observable, policy-bound, and subordinate to workflow control.

### A2A Protocol Model
The architecture may support agent-to-agent handoff, but only as structured A2A:

- one workflow step hands off to another bounded agent step
- the handoff carries standardized payload and shared-state references
- the receiving agent acts inside declared tool, autonomy, and approval constraints

In other words, A2A is workflow-mediated and contract-driven, not an open peer network.

## 11. Prompt Governance Intent
The target architecture should evolve toward a managed prompt layer with:

- family-level base prompt assets
- workflow-step prompt assets
- runtime composition rules for state, tools, approvals, tenant, and schema context
- prompt versioning and change tracking
- evaluation and rollback rules for prompt regressions

This prompt layer is now modeled in runtime contracts/config, but broad prompt authoring is still not required before the current contract and workflow-alignment work is complete.

## 12. Production Readiness Control Areas
The following control areas are required for production readiness and extend the current MVP architecture:

- authentication, secrets, and token lifecycle
- audit trail and execution traceability
- automated testing and migration validation
- observability and failure diagnosis
- authorization and approval policy enforcement
- multi-tenant hardening and isolated operational controls
- model governance
- input/output safety controls
- frontend operational maturity beyond the current `shadcn/ui` mission-control baseline
- data lifecycle management
- deployment packaging and implementation runbooks

## 13. Production Control Intent
### Authorization
The MVP single-approver model will evolve toward role-based permissions, delegated authority, approval classes, and workflow-specific policy enforcement.

### Audit and Traceability
The platform must preserve trustworthy traces for workflow execution, approvals, model/provider choice, routing path, fallback mode, assistant recommendation-to-task promotion, and outbound actions.

### Observability
Production operation requires:
- structured logs
- per-workflow metrics
- connector health visibility
- routing/fallback visibility
- alerting on critical workflow, send, approval, and retrieval failures

### Safety Controls
Generative workflows that create external communications must include:
- prompt-injection defensive patterns
- structured input validation
- outbound content validation
- grounded retrieval where applicable
- explicit review gates for risky outputs

### Data Lifecycle
The platform must define:
- retention periods by data class
- archival and deletion procedures
- backup frequency
- restore procedures and validation
- residency and storage boundary assumptions

### Multi-Tenant Enforcement
Isolation must be enforced through:
- tenant bootstrap automation
- separate secrets and runtime configuration
- isolated storage boundaries
- backup/restore per instance
- tenant-specific observability and operational controls



See [MEMORY_MODEL.md](c:/Users/dpizz/OneDrive/Python/AI Business/MEMORY_MODEL.md) for the full shared-brain definition and consistency rules.
See [PROMPTS.md](c:/Users/dpizz/OneDrive/Python/AI Business/PROMPTS.md) for canonical prompt naming, storage, and loading conventions.
See [PODS.md](c:/Users/dpizz/OneDrive/Python/AI Business/PODS.md) for pod ownership and reuse rules.
See [PLATFORM_MODEL.md](c:/Users/dpizz/OneDrive/Python/AI Business/PLATFORM_MODEL.md), [STATE_MODEL.md](c:/Users/dpizz/OneDrive/Python/AI Business/STATE_MODEL.md), [TOOLS.md](c:/Users/dpizz/OneDrive/Python/AI Business/TOOLS.md), [AUTONOMY_MODEL.md](c:/Users/dpizz/OneDrive/Python/AI Business/AUTONOMY_MODEL.md), and [EVENT_MODEL.md](c:/Users/dpizz/OneDrive/Python/AI Business/EVENT_MODEL.md) for the formal operating meta-model added through the handoff integration.
