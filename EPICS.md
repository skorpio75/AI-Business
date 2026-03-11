# Epics

## Epic 1 - Project Foundation
### Outcome
A clean repo, documentation system, and project conventions.

### Main tech components
- Markdown
- Git
- Docker Compose

### Acceptance criteria
- starter docs exist
- repo structure is fixed
- naming conventions are documented
- two-track scope is documented

## Epic 2 - Core Platform Foundation
### Outcome
A runnable backend with config, persistence, and model access.

### Main tech components
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- LiteLLM
- Pydantic Settings

### Acceptance criteria
- API starts locally
- DB migrations work
- config loads from files and env
- model gateway can answer a test prompt

## Epic 3 - Workflow Engine
### Outcome
Reusable deterministic workflows with approval checkpoints.

### Main tech components
- LangGraph
- Pydantic

### Acceptance criteria
- workflow graph runs end to end
- approval checkpoint exists
- workflow state is persisted

## Epic 4 - Knowledge Layer
### Outcome
Documents can be ingested and used for grounded answers.

### Main tech components
- LlamaIndex
- Unstructured
- pgvector
- PostgreSQL

### Acceptance criteria
- documents ingest successfully
- embeddings are stored
- retrieval returns relevant chunks

## Epic 5 - Track A Internal Operations MVP
### Outcome
The internal business can run key workflows with one human approver.

### Main tech components
- React
- FastAPI
- LangGraph
- LiteLLM
- Langfuse

### Acceptance criteria
- inbox workflow works
- knowledge workflow works
- proposal workflow produces drafts
- approval UI is usable

## Epic 6 - Track B Client Template MVP
### Outcome
A reproducible isolated client platform can be deployed quickly.

### Main tech components
- Docker Compose
- YAML
- FastAPI
- PostgreSQL

### Acceptance criteria
- client config pack exists
- deployment can be cloned
- seed scripts prepare first instance
- workflows run with client-specific context

## Epic 7 - Observability
### Outcome
The platform provides traces and debugging visibility.

### Main tech components
- Langfuse

### Acceptance criteria
- workflow traces visible
- prompt traces visible
- model usage visible

## Epic 8 - Testing Foundation
### Outcome
Reliable automated tests for core modules and workflows.

### Main tech components
- pytest
- httpx

### Acceptance criteria
- unit tests run locally
- integration tests cover API endpoints
- workflow tests cover main branches

## Epic 9 - Later Ops Automation
### Outcome
Controlled delivery pipeline with agent support for repetitive engineering work.

### Main tech components
- Git
- GitHub Actions or GitLab CI
- Ruff
- mypy
- pre-commit

### Acceptance criteria
- CI runs on push
- lint and tests run automatically
- release checklist is documented
- ops automation backlog exists
