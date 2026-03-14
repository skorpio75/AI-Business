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
4. memory/context is assembled from shared workspace and knowledge layer
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

### Approval-bound execution
- Microsoft Graph reply send for approved Outlook-originated email workflows

These connectors are selected through environment settings. Write actions remain approval-bound in MVP and execute only through platform-controlled paths after approval is recorded here.

## Current Integration Gaps
- OAuth/bootstrap flow for Gmail, Google Calendar, and Microsoft Graph
- secret storage and rotation strategy
- refresh-token lifecycle handling across providers
- connector diagnostics for token/bootstrap state beyond the current health views
