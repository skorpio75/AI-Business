<!-- Copyright (c) Dario Pizzolante -->
﻿# Enterprise Agent Platform MVP - Two-Track Blueprint

## Current Implementation Note

This blueprint describes the target platform shape. Current execution status and task sequencing live in `ROADMAP.md` and `TODO.md`, and governance/runtime truth lives in `AGENTS.md`, `AGENT_LLM_ROUTING_MATRIX.md`, `ARCHITECTURE.md`, and `DECISIONS.md`.

Treat this file as a reference blueprint, not the live implementation tracker.

As of 2026-03-16:
- Phase 3 (`Track A Internal MVP Workflows`) is complete.
- Phase 4 (`Track B Client Template MVP`) is in progress.
- Mission Control is implemented in `frontend/` as a React operator console using `shadcn/ui` + Tailwind.
- Email operations, internal knowledge Q&A, proposal generation, specialist advisory panels, and client-context specialist analysis endpoints are implemented in the internal instance.
- Provider-backed Gmail, Google Calendar, and Microsoft Graph read connectors are in place, and approved Outlook replies can send through Microsoft Graph after platform approval.
- The current model-routing reality is mixed: `ModelGateway` remains the shared runtime layer, LiteLLM remains the cloud/provider abstraction path, and some latency-sensitive local specialist-panel calls now use direct Ollama requests with compact prompts and explicit local-model overrides.
- Agent-family routing posture is documented separately in `AGENT_LLM_ROUTING_MATRIX.md` so the direct-Ollama pattern is expanded selectively rather than assumed for every family.
- For exact implementation truth, prefer `ROADMAP.md`, `TODO.md`, and the service code over this reference blueprint.

## 1. Objective

Build a reproducible, privacy-isolated enterprise agent platform with two parallel tracks:

- **Track A â€” Internal Instance**: run the freelance company with agents, with one human approver.
- **Track B â€” Client Instance Template**: reusable client-ready platform blueprint, deployed separately per client.

Constraints:

- open source only
- remote model usage allowed when needed
- isolated deployment per client
- markdown-first project structure
- later extension for LLMOps, MLOps, CI/CD, Git, and agent-managed operations

---

## 2. Top-Down Architecture

### Layer 1 â€” Interfaces

- Mission Control operator console (`frontend/`)
- FastAPI endpoints
- webhooks / scheduled jobs

### Layer 2 â€” Workflows

- deterministic workflows
- human approval checkpoints
- reusable workflow templates

### Layer 3 â€” Agent Modules

- email agent
- knowledge agent
- document agent
- reporting agent
- internal ops agent

### Layer 4 â€” Platform Foundation

- model gateway
- knowledge ingestion
- retrieval
- connectors
- configuration system
- observability

### Layer 5 â€” Infrastructure

- PostgreSQL
- pgvector
- Docker Compose
- local file/object storage
- Langfuse

---

## 3. Minimal Core Stack

### Main tech components

- **FastAPI**
- **React**
- **shadcn/ui**
- **Tailwind**
- **LangGraph**
- **LiteLLM** for cloud/provider abstraction
- **Ollama** for direct local-model execution where needed
- **LlamaIndex**
- **PostgreSQL**
- **pgvector**
- **Langfuse**
- **Docker Compose**
- **Pydantic / Pydantic Settings**
- **Jinja2**
- **SQLAlchemy**
- **Alembic**

---

## 4. Track A â€” Internal Instance

### Purpose

Create an agent-assisted operating system for the freelance business, with the user as sole approver.

### Priority workflows

1. **Inbox triage and draft replies**
2. **Proposal / statement of work generation**
3. **Internal knowledge search**
4. **Task and daily ops summary**
5. **Reporting and follow-up generation**

### Main tech components

- React UI
- shadcn/ui
- Tailwind
- FastAPI
- LangGraph
- LiteLLM
- PostgreSQL
- pgvector
- LlamaIndex
- Langfuse

---

## 5. Track B â€” Client Instance Template

### Purpose

Create a reproducible client-ready platform template that can be deployed in isolated environments.

### Priority reusable use cases

1. **Email Operations Agent**
2. **Internal Knowledge Agent**
3. **Document Intake Agent**
4. **Reporting Agent**

### Main tech components

- same as Track A
- plus configuration packs
- plus deployment templates
- plus client-specific ingestion pipelines

---

## 6. Reuse Model

### Shared across all deployments

- codebase
- architecture
- agent templates
- workflow templates
- configuration schema
- deployment scripts
- documentation structure

### Isolated per instance

- database
- vector data
- credentials
- documents
- logs
- prompts if needed
- connectors if needed

---

## 7. Repository Structure

```text
enterprise-agent-platform/
|- README.md
|- ROADMAP.md
|- EPICS.md
|- ARCHITECTURE.md
|- AGENTS.md
|- AGENT_LLM_ROUTING_MATRIX.md
|- WORKFLOWS.md
|- DECISIONS.md
|- TODO.md
|- .env.example
|- docker-compose.yml
|- Makefile
|- docs/
|  |- vision.md
|  |- platform-foundation.md
|  |- deployment-model.md
|  |- llmops-mlops-later.md
|  `- testing-strategy.md
|- config/
|  |- base/
|  |  |- platform.yaml
|  |  |- models.yaml
|  |  |- agents.yaml
|  |  `- workflows.yaml
|  |- internal/
|  |  `- company.yaml
|  `- client-template/
|     `- client.yaml
|- prompts/
|  |- email/
|  |- knowledge/
|  |- document/
|  `- reporting/
|- agents/
|  |- email-agent.md
|  |- knowledge-agent.md
|  |- document-agent.md
|  |- reporting-agent.md
|  `- ops-agent.md
|- workflows/
|  |- email-operations.md
|  |- knowledge-qna.md
|  |- document-intake.md
|  `- reporting.md
|- app/
|  |- api/
|  |- core/
|  |- orchestration/
|  |- connectors/
|  |- knowledge/
|  |- models/
|  |- observability/
|  |- db/
|  `- services/
|- frontend/
|- tests/
|  |- unit/
|  |- integration/
|  `- workflow/
`- scripts/
   |- ingest_docs.py
   |- init_db.py
   `- seed_config.py
```

---

## 8. Markdown-First Documentation Model

### `README.md`

Purpose:

- project overview
- local startup
- stack summary
- repo conventions

### `ROADMAP.md`

Purpose:

- phases
- milestones
- sequencing
- later-stage ops roadmap

### `EPICS.md`

Purpose:

- epics
- business outcomes
- acceptance criteria
- status tracking

### `ARCHITECTURE.md`

Purpose:

- top-down architecture
- module boundaries
- deployment model
- isolation model

### `AGENTS.md`

Purpose:

- list of all agents
- responsibilities
- inputs/outputs
- approval rules

### `AGENT_LLM_ROUTING_MATRIX.md`

Purpose:

- family-level LLM routing posture
- compact direct-Ollama vs guarded local drafting vs richer governed gateway reasoning vs deterministic hybrids
- rollout-wave planning for future adoption

### `WORKFLOWS.md`

Purpose:

- canonical reusable workflows
- step-by-step graphs
- AI vs deterministic steps

### `DECISIONS.md`

Purpose:

- architecture decisions log
- trade-offs
- deferred decisions

### `TODO.md`

Purpose:

- short-term implementation backlog

### `agents/*.md`

Purpose:

- one markdown spec per agent
- role, tools, prompts, inputs, outputs, constraints

### `workflows/*.md`

Purpose:

- one markdown spec per workflow
- steps, branching, approval points, dependencies

---

## 9. Agent Spec Template

```md
# Agent: Email Agent

## Purpose
Draft and classify inbound email.

## Scope
- classify intent
- retrieve context
- propose draft
- never send without approval

## Inputs
- inbound email
- client/company context
- relevant knowledge chunks

## Outputs
- classification
- confidence
- suggested reply
- escalation flag

## Tools
- mailbox connector
- knowledge retrieval service
- logging service

## Human Approval
Required before send.

## Constraints
- no autonomous sending
- no external sharing
- cite retrieved evidence when available
```

---

## 10. Workflow Spec Template

```md
# Workflow: Email Operations

## Trigger
Inbound email received.

## Steps
1. ingest email
2. classify intent
3. retrieve knowledge
4. draft reply
5. score confidence
6. route to approval
7. send only after approval

## AI Steps
- classify intent
- draft reply

## Deterministic Steps
- ingest email
- retrieve documents
- approval routing
- send

## Failure Handling
- low confidence -> escalate
- missing knowledge -> manual review

## Audit Data
- email id
- classification
- prompt version
- model used
- approval decision
```

---

## 11. MVP Epics

### Epic 1 â€” Project Foundation

Outcome:

- bootstrapped repository and documentation system

Main tech components

- Git
- Markdown docs
- FastAPI skeleton
- Docker Compose

### Epic 2 â€” Core Platform Foundation

Outcome:

- base backend, config system, DB, model gateway

Main tech components

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- LiteLLM
- Pydantic Settings

### Epic 3 â€” Workflow Engine

Outcome:

- reusable workflow execution model

Main tech components

- LangGraph
- Pydantic

### Epic 4 â€” Knowledge Layer

Outcome:

- ingestion and retrieval for documents

Main tech components

- LlamaIndex
- pgvector
- PostgreSQL
- Unstructured

### Epic 5 â€” Internal MVP Workflows

Outcome:

- inbox, knowledge, proposal workflows working for internal use

Main tech components

- React
- LangGraph
- LiteLLM
- PostgreSQL

### Epic 6 â€” Client Template MVP

Outcome:

- isolated deployable client instance template

Main tech components

- Docker Compose
- config packs
- seed scripts

### Epic 7 â€” Observability

Outcome:

- traces, run history, prompt inspection

Main tech components

- Langfuse

### Epic 8 â€” Testing Foundation

Outcome:

- basic unit, integration, workflow tests

Main tech components

- pytest
- httpx
- test fixtures

### Epic 9 â€” Agent-Managed Ops Later

Outcome:

- agent support for testing, release preparation, runbook generation

Main tech components

- GitHub Actions later
- lint/test agents later
- CI/CD later

---

## 12. Roadmap

### Phase 0 â€” Documentation and Repo Skeleton

- create repo
- create markdown-first structure
- define conventions
- define MVP scope

### Phase 1 â€” Platform Core

- FastAPI app
- config loader
- DB models
- shared model gateway with LiteLLM-compatible cloud/provider routing
- Docker Compose

### Phase 2 â€” Workflow + Knowledge

- LangGraph base workflow engine
- document ingestion
- pgvector retrieval
- first shared services

### Phase 3 â€” Track A Internal MVP

- email operations workflow
- knowledge assistant workflow
- proposal workflow
- React approval UI

### Phase 4 â€” Track B Client Template MVP

- isolated deployment template
- client config pack
- seed + setup scripts
- reusable workflow packaging

### Phase 5 â€” Observability + Testing

- Langfuse integration
- pytest structure
- workflow test scenarios

### Phase 6 â€” Later Ops Layer

- Git workflow
- CI/CD
- automated tests in pipeline
- agent-assisted release operations
- LLMOps / MLOps processes

---

## 13. Later Layer to Keep in Mind

Not for the first build, but planned:

### LLMOps / MLOps / Delivery

- Git
- CI/CD
- automated testing
- evaluation datasets
- prompt versioning
- release process
- rollback process
- agent-assisted QA and ops

### Main tech components later

- **Git**
- **GitHub / GitLab CI**
- **pytest**
- **Ruff**
- **mypy**
- **pre-commit**
- **DVC or MLflow only if really needed later**

---

## 14. Recommended First Build Order

1. repo skeleton + markdown docs
2. Docker Compose + PostgreSQL + pgvector
3. FastAPI backend skeleton
4. LiteLLM integration
5. LangGraph workflow base
6. document ingestion + retrieval
7. React approval UI
8. internal email workflow
9. internal knowledge workflow
10. client deployment template
11. Langfuse tracing
12. tests

---

## 15. Immediate Next Deliverables

- `README.md`
- `ROADMAP.md`
- `EPICS.md`
- `ARCHITECTURE.md`
- `AGENTS.md`
- `WORKFLOWS.md`
- first agent spec: `agents/email-agent.md`
- first workflow spec: `workflows/email-operations.md`

---

## 16. Guiding Principle

Build **one clean open-source platform blueprint**, deploy it **separately per instance**, document everything in **descriptive markdown**, and evolve later toward **agent-assisted DevOps, LLMOps, MLOps, CI/CD, and automated testing** without over-engineering the MVP.

---

# Appendix A â€” Starter Markdown Files

## File: `README.md`

````md
# Enterprise Agent Platform

## Overview
This project is a reproducible, privacy-isolated enterprise agent platform designed for two parallel goals:

- **Track A â€” Internal Instance**: operate a freelance/consulting business with AI-assisted workflows and one human approver.
- **Track B â€” Client Instance Template**: deploy isolated, reusable agent-platform instances for end customers without rebuilding from scratch.

The platform is **not shared across clients**. Each instance is deployed separately for privacy, compliance, and operational clarity.

## Principles
- open source first
- isolated deployment per company
- markdown-first documentation
- deterministic workflows with AI inside key steps
- one human approval layer for sensitive actions
- reusable templates for agents and workflows
- minimal MVP, scalable architecture later

## Main Tech Components
- **FastAPI**
- **React**
- **LangGraph**
- **LiteLLM**
- **LlamaIndex**
- **PostgreSQL**
- **pgvector**
- **Langfuse**
- **Docker Compose**
- **SQLAlchemy**
- **Alembic**
- **Pydantic Settings**
- **Jinja2**

## Initial MVP Scope
### Track A
- inbox triage and reply drafting
- internal knowledge assistant
- proposal generation workflow
- approval dashboard

### Track B
- isolated client deployment template
- reusable email workflow
- reusable knowledge workflow
- reusable document intake workflow

## Repository Structure
```text
enterprise-agent-platform/
â”œâ”€ README.md
â”œâ”€ ROADMAP.md
â”œâ”€ EPICS.md
â”œâ”€ ARCHITECTURE.md
â”œâ”€ AGENTS.md
â”œâ”€ AGENT_LLM_ROUTING_MATRIX.md
â”œâ”€ WORKFLOWS.md
â”œâ”€ DECISIONS.md
â”œâ”€ TODO.md
â”œâ”€ docs/
â”œâ”€ config/
â”œâ”€ prompts/
â”œâ”€ agents/
â”œâ”€ workflows/
â”œâ”€ app/
â”œâ”€ tests/
â””â”€ scripts/
````

## Startup Goal

The first production goal is to deliver:

- one internal instance for real usage
- one client-ready deployment template
- one reusable workflow library

## Delivery Philosophy

Start with a small, serious foundation.
Do not over-engineer the first version.
Use deterministic workflows and keep AI tightly scoped.

## Later Expansion

Later phases will introduce:

- CI/CD
- Git workflow
- automated testing
- agent-assisted operations
- LLMOps / MLOps controls
- evaluation pipelines
- release governance

````

---

## File: `ARCHITECTURE.md`

```md
# Architecture

## 1. Top-Down View
The system is built as a reproducible enterprise agent platform blueprint with isolated deployments.

```text
Interfaces
   â†“
Workflows
   â†“
Agent Modules
   â†“
Platform Foundation
   â†“
Infrastructure
````

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

This means the platform is **reproducible**, not **multi-tenant shared**.

## 3. Layer Breakdown

### Interfaces

Purpose:
operator access, approvals, API consumption.

Main tech components:

- **React**
- **FastAPI**

### Workflows

Purpose:
coordinate deterministic process execution.

Main tech components:

- **LangGraph**

### Agent Modules

Purpose:
encapsulate narrow AI responsibilities.

Main tech components:

- **Python modules**
- **Pydantic**

### Platform Foundation

Purpose:
provide common services reused by all workflows.

Main tech components:

- **LiteLLM**
- **LlamaIndex**
- **PostgreSQL**
- **pgvector**
- **Langfuse**
- **Jinja2**
- **Pydantic Settings**

### Infrastructure

Purpose:
run and package the system per instance.

Main tech components:

- **Docker Compose**
- **PostgreSQL**
- local file storage

## 4. Core Functional Components

### API Layer

- exposes workflow endpoints
- exposes admin endpoints
- handles integration entry points

Main tech components:

- **FastAPI**

### Workflow Engine

- runs workflow graphs
- manages routing and checkpoints
- supports approval nodes

Main tech components:

- **LangGraph**

### Model Gateway

- standardizes model calls
- centralizes model config
- supports fallback later

Main tech components:

- **LiteLLM**

### Knowledge Layer

- ingests company documents
- creates embeddings
- retrieves relevant context

Main tech components:

- **LlamaIndex**
- **pgvector**
- **PostgreSQL**
- **Unstructured**

### Observability

- captures traces
- stores run history
- supports debugging

Main tech components:

- **Langfuse**

### Config Layer

- allows client-specific behavior without code rewrites

Main tech components:

- **YAML**
- **Pydantic Settings**
- **Jinja2**

## 5. MVP Workflows Supported

- email operations
- internal knowledge Q&A
- proposal generation
- document intake

## 6. Architectural Rule

AI should not control the full system autonomously.
The workflow controls the process.
AI is used only inside selected steps.

## 7. Later Expansion

Later layers may include:

- CI/CD
- evaluation services
- automated tests in pipeline
- agent-assisted release operations
- stronger IAM
- advanced observability

````

---

## File: `ROADMAP.md`

```md
# Roadmap

## Phase 0 â€” Repo and Documentation Foundation
### Objective
Create the markdown-first structure and project conventions.

### Deliverables
- repository skeleton
- README
- architecture document
- epics document
- workflow and agent specs
- config conventions

### Main tech components
- **Markdown**
- **Git**
- **Docker Compose**

---

## Phase 1 â€” Platform Core
### Objective
Build the minimum technical backbone.

### Deliverables
- FastAPI skeleton
- config loader
- PostgreSQL integration
- pgvector enabled
- LiteLLM setup
- Docker Compose stack

### Main tech components
- **FastAPI**
- **PostgreSQL**
- **pgvector**
- **LiteLLM**
- **SQLAlchemy**
- **Alembic**
- **Pydantic Settings**

---

## Phase 2 â€” Workflow + Knowledge Foundation
### Objective
Add workflow orchestration and knowledge retrieval.

### Deliverables
- LangGraph workflow base
- document ingestion script
- retrieval service
- prompt/config structure

### Main tech components
- **LangGraph**
- **LlamaIndex**
- **Unstructured**
- **pgvector**
- **Jinja2**

---

## Phase 3 â€” Track A Internal MVP
### Objective
Deploy the first working internal instance.

### Deliverables
- email operations workflow
- knowledge assistant workflow
- proposal workflow
- approval UI

### Main tech components
- **React**
- **FastAPI**
- **LangGraph**
- **LiteLLM** for cloud/provider routing
- **Ollama** for direct local execution on selected paths
- **PostgreSQL**
- **Langfuse**

---

## Phase 4 â€” Track B Client Template MVP
### Objective
Create the first isolated client deployment template.

### Deliverables
- client config pack
- deployment template
- seed scripts
- reusable workflow packaging

### Main tech components
- **Docker Compose**
- **YAML**
- **FastAPI**
- **PostgreSQL**

---

## Phase 5 â€” Observability and Tests
### Objective
Add reliability and traceability.

### Deliverables
- Langfuse traces
- unit tests
- integration tests
- workflow tests

### Main tech components
- **Langfuse**
- **pytest**
- **httpx**

---

## Phase 6 â€” Ops and Delivery Later
### Objective
Introduce controlled delivery and agent-assisted operations.

### Deliverables
- Git workflow
- CI/CD pipeline
- linting and type checks
- automated test runs
- agent-assisted QA support
- release notes automation
- LLMOps / MLOps conventions

### Main tech components
- **Git**
- **GitHub Actions** or **GitLab CI**
- **Ruff**
- **mypy**
- **pre-commit**
- **pytest**

---

## Milestone Sequence
1. repo foundation
2. core platform
3. workflow engine
4. knowledge layer
5. internal instance live
6. client template live
7. observability and tests
8. ops automation later
````

---

## File: `EPICS.md`

```md
# Epics

## Epic 1 â€” Project Foundation
### Outcome
A clean repo, documentation system, and project conventions.

### Main tech components
- **Markdown**
- **Git**
- **Docker Compose**

### Acceptance criteria
- starter docs exist
- repo structure is fixed
- naming conventions are documented
- two-track scope is documented

---

## Epic 2 â€” Core Platform Foundation
### Outcome
A runnable backend with config, persistence, and model access.

### Main tech components
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **LiteLLM**
- **Pydantic Settings**

### Acceptance criteria
- API starts locally
- DB migrations work
- config loads from files and env
- model gateway can answer a test prompt

---

## Epic 3 â€” Workflow Engine
### Outcome
Reusable deterministic workflows with approval checkpoints.

### Main tech components
- **LangGraph**
- **Pydantic**

### Acceptance criteria
- workflow graph runs end to end
- approval checkpoint exists
- workflow state is persisted

---

## Epic 4 â€” Knowledge Layer
### Outcome
Documents can be ingested and used for grounded answers.

### Main tech components
- **LlamaIndex**
- **Unstructured**
- **pgvector**
- **PostgreSQL**

### Acceptance criteria
- documents ingest successfully
- embeddings are stored
- retrieval returns relevant chunks

---

## Epic 5 â€” Track A Internal Operations MVP
### Outcome
The internal business can run key workflows with one human approver.

### Main tech components
- **React**
- **FastAPI**
- **LangGraph**
- **LiteLLM**
- **Langfuse**

### Acceptance criteria
- inbox workflow works
- knowledge workflow works
- proposal workflow produces drafts
- approval UI is usable

---

## Epic 6 â€” Track B Client Template MVP
### Outcome
A reproducible isolated client platform can be deployed quickly.

### Main tech components
- **Docker Compose**
- **YAML**
- **FastAPI**
- **PostgreSQL**

### Acceptance criteria
- client config pack exists
- deployment can be cloned
- seed scripts prepare first instance
- workflows run with client-specific context

---

## Epic 7 â€” Observability
### Outcome
The platform provides traces and debugging visibility.

### Main tech components
- **Langfuse**

### Acceptance criteria
- workflow traces visible
- prompt traces visible
- model usage visible

---

## Epic 8 â€” Testing Foundation
### Outcome
Reliable automated tests for core modules and workflows.

### Main tech components
- **pytest**
- **httpx**

### Acceptance criteria
- unit tests run locally
- integration tests cover API endpoints
- workflow tests cover main branches

---

## Epic 9 â€” Later Ops Automation
### Outcome
Controlled delivery pipeline with agent support for repetitive engineering work.

### Main tech components
- **Git**
- **GitHub Actions** or **GitLab CI**
- **Ruff**
- **mypy**
- **pre-commit**

### Acceptance criteria
- CI runs on push
- lint and tests run automatically
- release checklist is documented
- ops automation backlog exists
```

---

## 17. Control Dashboard (Mission Control)

### Purpose

Provide a central operational interface similar to a **"Mission Control" dashboard** to supervise the platform, workflows, agents, and approvals.

This dashboard becomes the **human control layer** of the agent platform.

It allows the operator to:

- monitor running workflows
- approve or reject actions
- inspect agent reasoning traces
- monitor model usage
- trigger workflows manually
- review system health

### Role in Architecture

```text
Mission Control Dashboard
        â”‚
        â–¼
API Layer (FastAPI)
        â”‚
        â–¼
Workflow Orchestrator (LangGraph)
        â”‚
        â–¼
Agents / Tools / Knowledge
```

The dashboard interacts with the platform through the **API layer**.

### Main Tech Components

- **React** (MVP UI)
- **FastAPI** (backend APIs)
- **Langfuse** (trace inspection)
- **PostgreSQL** (workflow state and approvals)

### MVP Features

#### Workflow Monitor

- running workflows
- status and duration
- success / failure state

#### Approval Queue

- pending approvals
- draft outputs
- approve / reject / edit

#### Agent Activity

- recent agent runs
- prompts and responses
- model used

#### System Health

- connector status
- ingestion jobs
- queue status

#### Manual Triggers

- run workflow manually
- test agents

### Later Expansion

- role-based access control
- multi-user operator view
- analytics dashboards
- cost monitoring
- workflow editing UI

---

## Appendix B â€” Immediate Next Files

## File: `AGENTS.md`

```md
# Agents

## Purpose
This document lists the canonical agents used by the platform.

## Core Agents
### Email Agent
Purpose:
- classify inbound email
- retrieve context
- draft replies
- escalate low-confidence cases

Main tech components
- **LangGraph**
- **LiteLLM**
- **FastAPI connectors**

### Knowledge Agent
Purpose:
- answer grounded questions from internal documents
- provide evidence-backed outputs

Main tech components
- **LlamaIndex**
- **pgvector**
- **LiteLLM**

### Document Agent
Purpose:
- classify documents
- extract structured data
- route for processing

Main tech components
- **Unstructured**
- **LangGraph**
- **LiteLLM**

### Reporting Agent
Purpose:
- generate summaries and periodic reports
- consolidate structured inputs

Main tech components
- **Python services**
- **LiteLLM**
- **PostgreSQL**

### Ops Agent
Purpose:
- assist with internal operations later
- generate runbooks, checklists, and test support artifacts

Main tech components
- **Markdown specs**
- **Git integrations later**

## Approval Principle
No sensitive external action is sent automatically in MVP.
A human approver validates before execution.
```

---

## File: `WORKFLOWS.md`

```md
# Workflows

## Purpose
This document lists the reusable workflow templates.

## Workflow 1 â€” Email Operations
Steps:
1. ingest email
2. classify intent
3. retrieve knowledge
4. draft reply
5. confidence check
6. approval
7. send

Main tech components
- **LangGraph**
- **LiteLLM**
- **LlamaIndex**
- **FastAPI connectors**

## Workflow 2 â€” Knowledge Q&A
Steps:
1. receive question
2. retrieve relevant chunks
3. synthesize answer
4. return with evidence

Main tech components
- **LlamaIndex**
- **pgvector**
- **LiteLLM**

## Workflow 3 â€” Document Intake
Steps:
1. upload document
2. extract text
3. classify
4. extract fields
5. validate
6. store result

Main tech components
- **Unstructured**
- **LangGraph**
- **PostgreSQL**
- **LiteLLM**

## Workflow 4 â€” Proposal Generation
Steps:
1. collect opportunity data
2. load reusable context
3. generate proposal draft
4. review and approve

Main tech components
- **LangGraph**
- **LiteLLM**
- **Jinja2**
- **PostgreSQL**
```

---

## File: `agents/email-agent.md`

```md
# Agent: Email Agent

## Purpose
Classify inbound emails, retrieve relevant context, and draft suggested replies.

## Scope
- classify intent
- identify urgency
- retrieve relevant knowledge
- draft reply
- escalate when confidence is low

## Inputs
- email subject
- email body
- sender metadata
- company context
- retrieved knowledge chunks

## Outputs
- intent category
- confidence score
- suggested draft
- escalation flag

## Tools
- mailbox connector
- retrieval service
- logging service

## Human Approval
Required before any outbound response.

## Constraints
- never send directly in MVP
- never invent facts when knowledge is missing
- escalate on ambiguity
```

---

## File: `workflows/email-operations.md`

```md
# Workflow: Email Operations

## Trigger
A new inbound email is received.

## Goal
Produce a grounded draft reply and route it for approval.

## Steps
1. ingest inbound email
2. classify intent
3. retrieve relevant knowledge
4. generate draft reply
5. assign confidence score
6. route to approval queue
7. send only after approval

## AI Steps
- intent classification
- reply drafting
- confidence estimation

## Deterministic Steps
- email ingestion
- retrieval call
- approval routing
- outbound send
- audit logging

## Failure Handling
- missing knowledge -> manual review
- low confidence -> escalate
- connector failure -> retry then manual review

## Audit Data
- inbound message id
- workflow id
- prompt version
- model used
- confidence score
- approval status
```

