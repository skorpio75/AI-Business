# Architecture

## 1. Top-Down View
The system is built as a reproducible enterprise agent platform blueprint with isolated deployments.

```text
Interfaces
  ->
Workflows
  ->
Agent Modules
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
- React operator console
- FastAPI endpoints

### Workflows
- LangGraph orchestration

### Agent Modules
- Python modules
- Pydantic contracts

### Platform Foundation
- LiteLLM
- LlamaIndex
- PostgreSQL
- pgvector
- Langfuse
- Jinja2
- Pydantic Settings

### Infrastructure
- Docker Compose
- PostgreSQL
- local file storage

## 4. MVP Workflows Supported
- email operations
- internal knowledge Q&A
- proposal generation
- document intake
- billing and collections
- finance reporting
- procurement (PO)
- project delivery control
- quality/testing gate
- documentation handover

## 5. Architectural Rule
The workflow controls the process. AI is used only inside selected steps.

## 6. Operating Model
- Single human CEO approval authority for high-risk actions.
- Agent modules are organized into two domains:
  - corporate functions (billing, finance, reporting, PO, compliance)
  - service delivery functions (PM, delivery, quality, consulting, documentation, testing)
- Mission Control UI is the operational control layer for visibility, approval, and audit.

## 7. Memory Model
- Working memory: active workflow state and approval checkpoints.
- Episodic memory: past runs, approvals, and traces.
- Semantic memory: retrieved knowledge from documents and vector search.
- Shared workspace: current operational truth for clients, projects, tasks, invoices, and related entities.

See [MEMORY_MODEL.md](c:/Users/dpizz/OneDrive/Python/AI Business/MEMORY_MODEL.md) for the full shared-brain definition and consistency rules.
