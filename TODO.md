# TODO

## Current Focus
- Active phase: `Phase 5 - Observability + Testing`
- Active cross-cutting stream: `AI-Business IDE handoff integration`
- Immediate goal: align audit and trace payloads with normalized events, tool IDs, autonomy classes, and approval classes

## Now
- [x] `H-T01` Create the missing meta-model docs from `AI-Business_IDE_Handoff.md`
- [x] `H-T02` Update governance docs to adopt the 4-pod model and normalized event/state/tool/autonomy language
- [x] `P3-T01` Scaffold React mission-control app
- [x] `P3-T02` Build workflow monitor page
- [x] `P3-T03` Build approval queue page
- [x] `P3-T04` Build agent activity page
- [x] `P3-T05` Implement email operations workflow end-to-end
- [x] `P3-T06` Implement knowledge Q&A workflow end-to-end
- [x] `P3-T07` Implement proposal generation workflow baseline
- [x] `P3-T08` Connect approval actions from UI to API

## Next
- [ ] `P5-T11` Align audit/trace model with normalized events, tool IDs, autonomy classes, and approval classes

## Soon After
- [ ] `B-T27A` Enrich the Agent Activity page with operating model and runtime posture labels
- [ ] `B-T50B` Add portfolio view keys, API client methods, and TypeScript contracts for `Clients`, `Engagements`, `Missions`, and `Mission Detail`
- [ ] `B-T50E` Build the `Missions` page as the first portfolio operating surface
- [ ] `B-T50F` Build the `Mission Detail` cockpit over roster, quality gates, approvals, and run activity
- [ ] `B-T50C` Build the `Clients` portfolio page
- [ ] `B-T50D` Build the `Engagements` portfolio page
- [ ] `B-T02A` Add a Microsoft To Do section to `Inbox & Calendar` using the same Microsoft Graph tenant/client context
- [ ] `B-T02B` Route assistant recommendation-to-task promotion through priority approval before writing Microsoft To Do
- [ ] `B-T51` Define source adapters and normalization contracts for lead spotting across manual and non-manual channels
- [ ] `B-T52` Add lead-candidate dedupe and materialization rules before canonical `lead.received`
- [ ] `B-T55` Define the `dispatch_candidate_plan` contract between signed scope and mission startup
- [ ] `B-T56` Define the `approved_consultant_roster` contract and Track B visibility model for dispatched consultants
- [ ] `B-T57` Define `billing_plan` contracts for the approved billing method
- [ ] `B-T58` Build the signed-scope to mission-start workflow with dispatch approval and roster activation
- [ ] `B-T63` Add mission-phase delivery quality gates for implementation, milestone release, and handoff readiness
- [ ] `B-T40` Define hybrid retrieval source classes and provenance rules for internal, client, and external evidence
- [ ] `B-T45` Define bounded review/gate agent step contracts for `approve`, `revise`, `escalate`, and `human_review`
- [ ] `B-T47` Define a formal agent-instance registry keyed by family, tenant, client, engagement, and mission
- [ ] `B-T49` Build a Track A portfolio summary feed over isolated client runtimes
- [ ] `H-T04` Reflect normalized metadata in later runtime/UI surfaces without disrupting current MVP delivery work
- [ ] `B-T01A` Apply the compact direct-Ollama local-first pattern to Knowledge Q&A
- [ ] `B-T01B` Apply the compact direct-Ollama local-first pattern to proposal drafting
- [ ] `B-T01C` Evaluate email drafting for the same Ollama path with stronger output guardrails

## Recently Finished
- [x] `B-T50A` Add `docs/mission-control-portfolio-ui-map.md` with the concrete UI map for `Clients`, `Engagements`, `Missions`, and `Mission Detail`, including proposed view keys, API shapes, and page/component structure
- [x] `B-T62` Define the mission `quality_gate_plan` contract in backend/config, link `project_state` to quality-gate plans and results, and add a governed Track B default template
- [x] `P5-T07` Define `AUDIT_MODEL.md` for canonical `agent_run`, `audit_event`, audit event family, and trace-linkage rules
- [x] `P5-T06` Add explicit `README.md` test execution instructions for the full suite plus the unit, integration, and workflow layers
- [x] `P5-T05` Add shared test fixtures and sample data builders for email, approval, knowledge, proposal, connector-status, and Track B runtime test shapes
- [x] `P5-T04` Add workflow branch tests for approval and escalation paths
- [x] `P5-T03` Add in-process FastAPI integration tests with DB dependency overrides and targeted service/startup patching
- [x] `P5-T02` Add a lightweight shared unit-test base structure for repo-root access, settings construction, temp dirs, in-memory DB sessions, and Track B seeded-client lifecycle helpers
- [x] `P5-T01` Add optional Langfuse tracing for workflow spans and nested `ModelGateway` generation observations, with env-gated settings and unit coverage
- [x] `P4-T06` Document the Track B client bootstrap runbook, including tenant env activation, startup, connector bootstrap, verification, and cleanup
- [x] `P4-T05` Validate workflow portability across seeded client instances by running reusable workflows under tenant-scoped runtime settings and checking the seeded workflow pack contract
- [x] `P4-T03` Build the client initialization seed script to generate tenant-specific client contracts, runtime env files, and tenant directory roots
- [x] `P4-T04` Isolate storage and credentials per client instance by enforcing tenant-scoped runtime env files, storage roots, prompt roots, and secret paths
- [x] `P4-T02` Finalize `config/client-template/client.yaml` with tenant, governance, deployment, storage, connector, routing, and default workflow/service sections
- [x] `P4-T01` Create the first Track B client deployment template pack with a pack README, client-scoped env template, compose overlay, and storage/secret path map
- [x] `B-T01-INV` Create `AGENT_LLM_ROUTING_MATRIX.md` and expand direct-Ollama planning from a few endpoints into a broader family-level candidate inventory aligned with `AGENTS.md`
- [x] Make the shared model timeout configurable via `.env`, split the heavy CTO/CIO and Chief AI internal panel generation into smaller section calls, and simplify those sections into compact local-first prompts that complete on the faster local Ollama model
- [x] `P4-T01D` Route internal CTO/CIO and Chief AI specialist panels through the governed prompt/model layer and surface routing metadata
- [x] `P4-T01C` Route CTO/CIO and Chief AI specialist analysis through the governed prompt/model layer with deterministic fallback guardrails
- [x] `P4-T01B` Extend CTO/CIO and Chief AI advisory analysis with consulting-style mission framing and upsell opportunity detection
- [x] `P4-T01A` Add typed CTO/CIO and Chief AI advisory-analysis endpoints so client-facing agents can assess a problem statement, context/history, and recommend relevant services
- [x] `P3-T14` Add a typed Chief AI / Digital Strategy endpoint and mission-control panel for AI opportunity portfolio, delivery blueprinting, and maturity guidance
- [x] `P3-T13` Add a typed finance cockpit endpoint and mission-control panel for accounting exceptions, close-readiness review, and CFO scenario cards
- [x] `P3-T12` Add a typed CTO/CIO specialist advisory endpoint and mission-control panel for customer scope insight, architecture guidance, strategy options, and internal improvement priorities
- [x] `P2-T20` Define canonical prompt asset naming, storage, and loading conventions with legacy explicit-path compatibility
- [x] `P2-T19` Add prompt-layer contracts/config for family-base assets, workflow-step assets, and runtime context injection, and wire the implemented prompt-backed services through the composable prompt loader
- [x] `P2-T18` Add normalized tool-permission profile contracts and config bindings by agent family/operating mode, and surface tool-profile metadata in the agent activity view
- [x] `P2-T17` Add typed backend ownership and persistence contracts for `opportunity_state`, `project_state`, `run_state`, and `approval_state`, and mirror the same mapping into base config
- [x] `P3-T16` Add provider bootstrap, secret handling, refresh-token lifecycle support, and bootstrap-status diagnostics for Google and Microsoft inbox/calendar connectors
- [x] `P2-T16` Add backend control-plane contracts for normalized event names, approval classes, and autonomy classes, and enrich workflow config with trigger/emitted-event/control metadata
- [x] `H-T03` Align the current markdown agent/workflow spec set with pod ownership, operating modes, state objects, emitted events, approval gates, and cross-agent handoff roles
- [x] `P2-T15` Align the runtime agent registry and base config with the pod model, family/mode/instance identity, and specialist-overlay mapping
- [x] Carry the PMO split into runtime-facing registry/config/contracts and surface pod/family/mode metadata in the agent activity view
- [x] Clarify the distinction between PMO governance/control and project-management execution coordination
- [x] `P3-T01A` Adopt `shadcn/ui` + Tailwind foundation and migrate shared mission-control UI primitives
- [x] `P3-T20` Add explicit routing badges for local model, cloud route, fallback-rule execution, and local LLM invocation status

## Watchlist
- [ ] Keep `ROADMAP.md` as the full source of truth
- [ ] Keep `TODO.md` short and execution-oriented
- [ ] Keep Track A internal instances and Track B client instances isolated even when they share an agent family
- [ ] Keep Track A portfolio visibility summary-only across client runtimes; do not turn it into shared mutable client state
- [ ] Treat raw commercial signals separately from materialized leads; `lead.received` should only fire after normalization, dedupe, and create-or-review decisioning
- [ ] Keep signed scope separate from mission startup; use approved dispatch planning, consultant roster activation, and billing-plan control in between
- [ ] Keep quality gates phase-aware and mission-specific; do not collapse document review, code review, test readiness, and handoff readiness into one generic late QA step
- [ ] Keep multi-agent runtime evolution workflow-first; avoid autonomous peer-agent complexity before step identity, handoff payloads, and execution logs are stable
- [ ] Treat the prompt layer as part of the target runtime architecture, but defer large-scale prompt authoring until contracts, state, and workflow boundaries are stable
- [ ] Reuse the compact direct-Ollama pattern selectively: best for bounded internal panels and short grounded outputs, not automatically for every richer client-facing reasoning surface
- [ ] Expand direct-Ollama planning by agent family: Executive synthesis, Delivery authoring, Growth/commercial drafting, and client-facing service variants should all be evaluated explicitly, not only the currently implemented endpoints
- [ ] Keep Microsoft Graph mail, calendar, and To Do scope aligned to the same tenant/client registration per instance unless an explicit isolation exception is documented
- [ ] Treat assistant recommendation-to-task promotion as an approval-bound external write, even when it targets the operator's own Microsoft To Do
- [ ] Use the high-suitability multi-agent matrix to prioritize runtime splitting instead of promoting all documented families at once
- [ ] Treat the medium-suitability set as bounded collaboration candidates, not immediate runtime-splitting priorities
- [ ] Avoid adding UI logic before API/contracts are stable enough to consume
