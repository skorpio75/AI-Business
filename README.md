# Enterprise Agent Platform

## Overview
This project is a reproducible, privacy-isolated enterprise agent platform designed for two parallel goals:

- Track A - Internal Instance: operate a freelance/consulting business with AI-assisted workflows and one human approver.
- Track B - Client Instance Template: deploy isolated, reusable agent-platform instances for end customers without rebuilding from scratch.

The platform is not shared across clients. Each instance is deployed separately for privacy, compliance, and operational clarity.

## Current Status
The committed codebase is currently backend-first. It includes the FastAPI API, workflow orchestration and database layer for the initial email-operations slice. A React operator UI is part of the target architecture, but it is not in this repository yet.

## Principles
- open source first
- isolated deployment per company
- markdown-first documentation
- deterministic workflows with AI inside key steps
- one human approval layer for sensitive actions
- reusable templates for agents and workflows
- minimal MVP, scalable architecture later

## Main Tech Components
- FastAPI
- LangGraph
- LiteLLM
- LlamaIndex
- PostgreSQL
- pgvector
- Langfuse
- Docker Compose
- SQLAlchemy
- Alembic
- Pydantic Settings
- Jinja2

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
|- README.md
|- ROADMAP.md
|- EPICS.md
|- ARCHITECTURE.md
|- AGENTS.md
|- WORKFLOWS.md
|- DECISIONS.md
|- TODO.md
|- .env.example
|- docker-compose.yml
|- Makefile
|- docs/
|- config/
|- prompts/
|- agents/
|- workflows/
|- app/
|- tests/
`- scripts/
```

## Startup Goal
Deliver one internal instance for real usage and one client-ready deployment template with reusable workflow specs.

## Delivery Philosophy
Start with a small, serious foundation. Do not over-engineer the first version.

## MVP Slice 1 (Working)
- Use case: inbox triage + draft reply + CEO approval.
- Backend: FastAPI endpoint for `email-operations`.
- Model routing: local-first (Ollama), optional cloud fallback (OpenRouter-compatible via LiteLLM).

## Local Run
1. Create and activate a virtual environment.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create the local environment file:
```bash
copy .env.example .env
```
4. Start PostgreSQL + pgvector:
```bash
make up
```
Default compose port is `5433` to avoid collisions with existing local PostgreSQL services.
5. Apply database migrations:
```bash
python scripts/init_db.py
```
6. Start API:
```bash
make api
```

Alternative DB command:
```bash
make db-upgrade
```

## API Endpoints (Current)
- `GET /healthz`
- `POST /workflows/email-operations/run`
- `GET /workflows/runs`
- `GET /approvals/pending`
- `POST /approvals/{approval_id}/decision`

## Git Hygiene
- Local secrets, virtual environments, caches, and local database files are intentionally excluded via `.gitignore`.
- Line endings are normalized through `.gitattributes` to keep Windows and GitHub diffs stable.
