<!-- Copyright (c) Dario Pizzolante -->
# Integrations

## Purpose
Define how external platforms and runtimes integrate with this system without breaking the platform's control model, shared workspace, or memory consistency.

## Integration Principle
External systems may provide channels, tools, device access, or specialized runtimes.
They must not become the source of truth for company state, approvals, or shared memory.

This platform remains the system of record for:
- workflows
- approvals
- shared workspace entities
- memory layers
- audit trail
- company operating state

## Integration Roles

### 1. Channel Layer
Used for communication ingress and egress.

Examples:
- email
- chat
- calendar
- messaging apps
- webhooks

### 2. Tool Layer
Used to execute bounded actions or retrieve data.

Examples:
- mailbox APIs
- calendar APIs
- accounting APIs
- CRM APIs
- file systems
- browser automation

### 3. Runtime Layer
Used when an external agent runtime or orchestration framework is helpful.

Examples:
- OpenClaw
- specialized automation runtimes
- external worker processes
- shared inference runtimes such as Track A local `Ollama`, shared Track B `Ollama`, or governed cloud model gateways

## OpenClaw Integration

### Recommended Role
OpenClaw should be treated as:
- a channel gateway
- a device/runtime execution layer
- an optional operator-facing access surface

OpenClaw should not be treated as:
- the shared brain
- the workflow system of record
- the approval authority
- the canonical source of company state

### Why
OpenClaw is well suited for session routing, messaging surfaces, and tool/plugin execution.
This platform is better suited to:
- structured business workflows
- memory consistency
- entity/state management
- approval enforcement
- auditability

Running both as equal orchestration centers would create split authority.

## Boundary Rules

### Rule 1
All business-critical state changes must flow through this platform's API/workflows.

### Rule 2
External runtimes may suggest, trigger, or execute bounded actions, but cannot independently commit authoritative business state.

### Rule 3
Approvals are always recorded and resolved in this platform.

### Rule 4
Shared memory promotion happens only here, not in external systems.

### Rule 5
External sessions may cache local context, but canonical context remains in this platform.

### Rule 6
External connectors and runtimes map their capabilities to normalized platform tool IDs and must not bypass the platform's approval, autonomy, or state rules.

### Rule 7
Client-facing advisory recommendations must be generated from a bounded client brief handled in this platform, even when external channels or tools supply part of the context.

### Rule 8
External systems may help gather account context, but consulting mission framing and upsell opportunity detection must remain platform-side so growth logic stays auditable and tenant-scoped.

### Rule 9
For Microsoft 365 personal-assistant flows, mailbox, calendar, and Microsoft To Do integration should reuse the same tenant, client ID, and operator account context unless an explicit isolation exception is documented.

### Rule 10
External web retrieval may broaden agent context and recommendations, but externally retrieved material must remain cited, distinguishable from internal or client-grounded sources, and non-authoritative unless later promoted through approved platform workflows.

### Rule 11
Shared inference infrastructure may be reused across isolated runtimes, but shared inference does not permit shared tenant state, shared retrieval, or shared mutable memory across clients.

## Inference Topology
The model-runtime layer should support an evolutive deployment path.

- Track A may start with its own internal `Ollama` endpoint for internal operations and delivery-lab work
- Track B may later use a shared `Ollama` inference service to reduce duplicated model-hosting cost across tenant runtimes
- cloud fallback should remain available through the governed `ModelGateway` and family-level routing posture
- shared inference should be treated as a runtime dependency, not as a shared state plane

## Deployment Evolution Rule
Cloud deployment should scale in stages rather than assuming a full client fleet on day one.

- first activate Track A production runtime, storage, database, and internal inference
- add Track B tenant runtimes only when real client missions are approved
- later introduce shared client inference, private networking, object storage, and per-tenant observability as client volume grows
- keep bootstrap and activation contracts explicit so later infrastructure scale-out does not force a change in operating semantics

## OpenClaw Interaction Pattern

### Pattern A: Event Ingress
OpenClaw receives a message or task from a channel and forwards a normalized event to FastAPI.

Examples:
- inbound email-like message
- assistant request from chat
- mobile command from CEO

### Pattern B: Approved Execution
This platform decides and records the action.
OpenClaw executes the approved action in the external channel/runtime.

Examples:
- send approved reply
- create draft in external tool
- fetch data from an external account

### Pattern C: Observability Bridge
This platform may publish workflow or approval summaries back to OpenClaw-facing channels for convenience.

Examples:
- CEO receives pending approvals in a messaging channel
- daily priority summary sent to assistant chat

## Canonical Ownership

### Owned by This Platform
- workflow state
- approvals
- company/project/client records
- financial and delivery state
- memory promotion
- audit trail

### Owned by OpenClaw
- channel sessions
- plugin/runtime execution details
- device-specific interaction state
- temporary channel context

## Data Flow
1. external message/task enters via OpenClaw or another connector
2. event is normalized and sent to FastAPI
3. workflow runs in this platform
4. memory/context is assembled from shared workspace, client brief inputs, and knowledge layer
5. approval is requested if needed
6. once approved, execution can be delegated back to OpenClaw or another tool connector
7. resulting state is written back here

## Good Integration Use Cases
- personal assistant access through chat/mobile channels
- messaging-based approval notifications
- delegated tool execution in external channels
- remote operator interaction with the platform

## Bad Integration Use Cases
- storing authoritative company memory only in OpenClaw sessions
- letting OpenClaw decide approvals
- duplicating workflow orchestration and state transitions in two systems
- maintaining a separate client/project truth outside this platform

## Initial Recommendation
Do not combine architectures at the core level.
Integrate OpenClaw later as an edge channel/runtime adapter after:
- workflow contracts are stable
- memory model is implemented
- approval model is stable
- provider auth/bootstrap and secret lifecycle are stable

## Future Integration Document Extensions
- connector-specific schemas
- auth and secret handling rules
- webhook contracts
- session correlation IDs
- error handling and retry policy

## Current Provider Support
The current backend supports the following provider capabilities:

### Read-side context ingestion
- Gmail inbox fetch via Google APIs
- Google Calendar event fetch
- Microsoft Graph mailbox fetch
- Microsoft Graph calendar fetch

These integrations may enrich a client advisory brief, but the normalized problem statement, client context/history, mission assessment, recommended services, and upsell opportunities remain platform-side contracts.

### Approval-bound execution
- Microsoft Graph reply send for approved Outlook-originated email workflows
- planned: Microsoft Graph Microsoft To Do task create/update for approved personal-assistant recommendation promotion and priority assignment

### Planned same-tenant Microsoft To Do extension
- `Inbox & Calendar` is planned to grow into an inbox, calendar, and task workspace when Microsoft 365 is the selected provider stack.
- Microsoft To Do list/task reads and writes should reuse the same Microsoft Graph tenant ID, client ID, and operator account context already used for Outlook mail and calendar.
- Assistant recommendations may become candidate tasks, but task creation and approved priority assignment must still flow through platform approval and audit controls before Microsoft To Do is updated.

### Bootstrap and secret handling
- Microsoft Graph device-code bootstrap via `scripts/microsoft_graph_device_code.py`
- Google local-loopback OAuth bootstrap via `scripts/google_oauth_local_server.py`
- refresh-token lifecycle handling for Google and Microsoft Graph
- optional JSON secret-store paths via `GOOGLE_SECRETS_PATH` and `MICROSOFT_GRAPH_SECRETS_PATH`
- client-scoped `RUNTIME_ENV_FILE` support so Track B token persistence follows the active tenant env file instead of the shared repo root `.env`
- bootstrap diagnostics through `GET /connectors/bootstrap-status`

These connectors are selected through environment settings. Write actions remain approval-bound in MVP and execute only through platform-controlled paths after approval is recorded here.

## Current Observability Integration
- Langfuse tracing is now supported as an optional external observability integration.
- The integration is env-gated through `LANGFUSE_ENABLED`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`, and optional `LANGFUSE_RELEASE`.
- Workflow/service spans are emitted for the current reusable workflow surfaces, and nested generation observations are emitted from the shared `ModelGateway` for local, cloud, and fallback routing paths.
- Track B client instances can configure Langfuse through their tenant-scoped runtime env file so tracing enablement follows the same per-instance bootstrap model as other runtime settings.
- If Langfuse is unconfigured or unavailable, tracing becomes a no-op rather than blocking workflow execution.

## Planned Hybrid Retrieval Boundary
- internal and tenant-scoped client corpora should remain the primary grounded retrieval layers for agent context
- external web retrieval is a planned enrichment layer for broader technology, vendor, standards, and market context
- hybrid retrieval outputs should preserve evidence provenance so operators can distinguish internal/client grounding from external enrichment
- risky externally consequential outputs should be able to route through a bounded review/gate step before approval or release

## Current Integration Gaps
- secret storage and rotation strategy
- connector-to-tool-ID mapping for normalized tool/audit contracts
- governed external web retrieval design with provenance, caching, and normalized tool mapping
- richer connector diagnostics in Mission Control UI beyond the current API and health/status surfaces
- Microsoft To Do list-selection, task-schema, and same-tenant recommendation-promotion contract design
- approval and audit trace design for recommendation-to-task promotion and priority write-back
