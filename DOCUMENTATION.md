# Project Documentation

This document covers the major topics the user requested.  It is intended to be exported to Word format (e.g. via `pandoc DOCUMENTATION.md -o documentation.docx`).

## Executive Summary

The Enterprise Agent Platform is a reusable, privacy-isolated foundation for running AI-assisted workflows within a small IT consultancy or deploying as a client-specific SaaS template.  It is built to support two parallel tracks:

1. **Track A – Internal Instance:** operate the developer's own freelance/consulting business with AI agents handling email triage, knowledge access, proposal generation, and other routine tasks under a single human CEO approver.
2. **Track B – Client Instance Template:** provision isolated, per-customer deployments using the same codebase, allowing each company to have its own database, documents, and credentials for compliance and privacy.

The platform's value proposition lies in accelerating operations through deterministic workflows that embed AI for classification, drafting, and decision support while ensuring auditability, approval gates, and extensibility. Target users include small professional services firms that need an affordable, license-free, open‑source automation backbone and software teams building custom agent-enabled solutions for clients.


## Technical Blueprint and Architecture

At a high level the platform composes several layers:

- **Interfaces:** a React‑based operator console for humans and FastAPI HTTP endpoints for workflow triggers and status.
- **Workflows:** business process definitions orchestrated by LangGraph, containing deterministic and AI‑enabled steps.
- **Agent Modules:** Python packages that implement individual reasoning capabilities, prompt templates, and Pydantic contracts.
- **Platform Foundation:** shared services such as LiteLLM for model execution, LlamaIndex for document retrieval, PostgreSQL with pgvector for embeddings, Langfuse tracing, Jinja2 templating, and Pydantic‑based configuration.
- **Infrastructure:** primarily Docker Compose powering a local PostgreSQL instance with pgvector, file storage for documents, and optional connectors for email or calendar APIs.

### Deployment Model

The codebase, configuration schema, and workflow/agent templates are shared across deployments, but each instance maintains isolation for data, credentials, and logs.  This ensures compliance and per‑customer customization while enabling rapid reuse.

### Architecture Diagram

*Add diagrams here referencing components above; typical flows include an email arriving at the FastAPI endpoint, being processed by a workflow, invoking agents, and finally updating the shared workspace.*

### Layer Breakdown

Refer to [ARCHITECTURE.md](ARCHITECTURE.md) for a formal description.  The platform adheres to the architectural rule: **the workflow controls the process; AI is used only inside selected steps.**


### Architecture Diagram

Insert or reference diagrams illustrating service boundaries, data flows, and hosting environment.

### Deployment Model

Explain infrastructure (cloud services, on‑prem, containers, etc.) and environment separation.

## Functional & Logical Components

The system is divided into these logical functional areas:

- **Ingestion / Connectors:** receive source data such as inbound email, documents, calendar events, or timesheets and normalize them into workflow inputs.
- **Workflow Orchestration:** manage the progression of a business process, sequentially executing steps, handling error paths, and raising approval checkpoints. Implemented via LangGraph state machines persisted in PostgreSQL.
- **Knowledge Store / Semantic Memory:** maintain indexed embeddings and metadata for documents and facts, enabling retrieval for grounding agent responses. Uses LlamaIndex backed by a pgvector store.
- **Shared Workspace:** relational representation of entities (clients, projects, invoices, tasks, approvals) that agents read and update through controlled workflow steps.
- **Agents / Reasoners:** encapsulate discrete capabilities like intent classification, reply drafting, financial analysis, and report generation. They are invoked by workflows with typed inputs/outputs.
- **User Interface:** React frontend provides visibility into active workflows, pending approvals, historical runs, and enables CEO interaction.
- **Approval Engine:** simple queue that holds items requiring human decision; approvals are recorded and can influence subsequent workflow paths.
- **Tracing and Observability:** Langfuse integration captures model prompts, outputs, and metadata for debugging and audit.


## Technical Components

Concrete technologies used throughout the platform include:

- **FastAPI** for the HTTP API layer hosting workflow triggers and status endpoints.
- **React** for the operator console (client-code lives outside this repository, but the UI interfaces with the API).
- **LangGraph** as the workflow engine, capturing step definitions, branching, and state persistence.
- **SQLAlchemy & Alembic** to model the relational schema and evolve the PostgreSQL database.
- **PostgreSQL with pgvector extension** to store embeddings and structured shared workspace data.
- **LiteLLM** as a local model runtime, with plug‑ins for cloud fallback (OpenRouter‑compatible) as needed.
- **LlamaIndex** for building indexes over ingested documents and performing vector retrievals.
- **Langfuse** for tracing AI calls, including prompt versions, model choices, and outputs.
- **Pydantic Settings** for configuration management across environments.
- **Jinja2** for template rendering inside prompts and report generation.
- **Docker Compose** as the default local deployment orchestrator; production deployments may use similar container stacks.
- **Python modules** under `app/` which contain business logic, agent definitions, and service wrappers (e.g. `app/services/email_workflow.py`).

Additional libraries include `psycopg2-binary`, `jinja2`, `requests`, and test frameworks such as `pytest` with custom integration tests.


## Data and Control Flows

### Email Workflow Example

1. **Incoming email** arrives via connector and POSTs to `POST /workflows/email-operations/run`.
2. FastAPI translates the request into initial workflow state and persists it.
3. LangGraph executes nodes:
   - `ingest inbound email` (deterministic store)
   - `classify intent` (calls Email Agent)
   - `retrieve relevant knowledge` (queries semantic memory via LlamaIndex)
   - `generate draft reply` (Email Agent drafts response using LiteLLM with enclosing templates)
   - `assign confidence score` (agent computes a numeric estimate)
   - `route to approval queue` (creates an approval record in shared workspace)
4. The CEO views pending approval in UI. On approval, the final action node sends the email out and logs the event.

### Document Intake & Knowledge Augmentation

Documents dropped into the `scripts/ingest_docs.py` pipeline are parsed, embedded, and stored in the vector index. Knowledge Agent queries this store during workflows to ground answers.

### Finance and Billing

Timesheets or deliverable records trigger workflows that call the Billing Agent to generate invoices. Upon CEO approval, the shared workspace updates invoice records and optionally sends notices.

All flows record audit data (prompt version, model used, confidence, workflow IDs) and optionally emit Langfuse traces for later inspection.


## Agentic Concepts

Agents are first‑class logical units encapsulating reasoning capabilities. They are not autonomous background processes; instead, they are pure functions invoked by workflows with clearly defined input and output contracts. Each agent consists of:

- a prompt template stored in `prompts/` or orchestrated via Jinja2,
- a Python wrapper that constructs the prompt, handles execution via LiteLLM, and parses the result,
- optional rankings or confidence estimators.

The platform enforces governance by:

- requiring any action that affects external systems or shared workspace state to pass through an approval checkpoint,
- restricting sensitive operations to human-approved workflows,
- isolating data per instance so agents cannot leak information between clients.

Agents are grouped by domain (corporate vs. service delivery) and by function (e.g., classification, drafting, analysis). The memory model ensures agents operate with contextual awareness by providing semantic memory for grounding and episodic records for reference.

### Agent Types and Roles

Refer to [AGENTS.md](AGENTS.md) for the canonical list.  Key roles include Email Agent for communication tasks, Finance/Billing agents for monetary processes, Knowledge and Consulting Support agents for research and Q&A, and a suite of delivery and quality agents to support project execution.


### Agent Types

- Email Agent
- Personal Assistant Agent
- Billing Agent
- Accountant Agent
- CFO Agent
- Finance Agent
- Procurement Agent
- Reporting Agent
- Compliance/Contract Agent
- CTO/CIO Agent
- Chief AI/Digital Strategy Agent
- Document Agent
- Knowledge Agent
- Project Management Agent
- Delivery Agent
- Quality Management Agent
- Consulting Support Agent
- Documentation Agent
- Testing/QA Agent
- Ops Agent

## Agents Implementation

Agents are principally defined within Python code under `app/` and configured via YAML files in the `config/` directory (e.g., `agents.yaml`). Prompts reside in the `prompts/` folder categorized by purpose (email, document, reporting).  A typical agent implementation includes:

- a Pydantic model for typed input and output,
- a service class (e.g. `app/services/email_workflow.py`) that composes prompts and calls the model runtime,
- an entry in `config/agents.yaml` specifying default model parameters and any routing rules.

Workflows embed agents as steps; LangGraph nodes reference a handler that calls the corresponding agent service.  Model routing is handled through a central gateway (`app/services/model_gateway.py`) which selects LiteLLM or cloud endpoints based on configuration and availability.

Tracing instrumentation (Langfuse) wraps agent calls to capture prompts, outputs, and metadata.  Developers can inspect traces to understand decision-making and debug issues.


## Other Topics

### Security and Access Control

- Environment variables and secrets are managed via `.env` files and Docker Compose; production deployments should use a secrets manager.
- The API exposes only authenticated endpoints; authentication can be added via OAuth or API keys.
- Agents run inside the same container but operate on isolated instance data; cross‑tenant data access is prevented by design.

### Observability and Monitoring

- Langfuse provides tracing for all AI interactions.
- PostgreSQL logs and metrics can be aggregated via the chosen host’s monitoring stack.
- Workflow run status and approval audits are queryable via the API and UI.

### Configuration Management

- Pydantic Settings classes centralize configuration with environment‑specific overrides in `config/`.
- YAML templates define agents, workflows, and platform options; they can be seeded per-client via the `scripts/seed_config.py` script.

### Testing Strategy

- `pytest` is used with unit tests under `tests/unit` and integration tests under `tests/integration`.
- Workflow tests exercise LangGraph definitions, and end‑to‑end tests simulate API calls.
- CI pipelines should run `make test` after running `make lint`.

### Change and Release Processes

- The codebase adheres to an open source first policy; changes are reviewed via GitHub PRs.
- Major architectural decisions are recorded in `DECISIONS.md` and tracked in `EPICS.md`.
- Releases are tagged in Git and can be deployed via Docker Compose or other container orchestrators.

### Data Governance and Privacy

- Each deployment is isolated to prevent data commingling.
- Sensitive documents and embeddings are stored locally and never sent to external services unless explicitly configured.
- Auditing of agent outputs and approval actions provides accountability.

### Roadmap and Extension Points

- Support additional connectors (Slack, Teams, calendar APIs).
- Expand the catalog of workflow templates for procurement, project delivery, and finance.
- Add multi-instance orchestration for managed services.
- Integrate identity and access management for multiple internal users.
- Enhance the UI with richer analytics and reporting.


---

*End of documentation template.*
