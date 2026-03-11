# Enterprise Agent Platform

## Overview
This project is a reproducible, privacy-isolated enterprise agent platform designed for two parallel goals:

- Track A - Internal Instance: operate a freelance/consulting business with AI-assisted workflows and one human approver.
- Track B - Client Instance Template: deploy isolated, reusable agent-platform instances for end customers without rebuilding from scratch.

The platform is not shared across clients. Each instance is deployed separately for privacy, compliance, and operational clarity.

## Current Status
The committed codebase is still backend-led. It includes the FastAPI API, workflow orchestration and database layer for the initial email-operations slice, plus an initial `frontend/` React mission-control scaffold with a workflow monitor, approval queue, and personal assistant summary fed by configurable inbox/calendar connectors.

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
|- frontend/
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
7. Start the frontend mission-control UI in a second terminal:
```bash
cd frontend
npm install
npm run dev
```

Alternative DB command:
```bash
make db-upgrade
```

## Windows PowerShell Run
If `make` is not installed, use the underlying commands directly from PowerShell.

Start PostgreSQL + pgvector:
```powershell
docker compose up -d
```

Apply database migrations:
```powershell
.venv\Scripts\python.exe scripts\init_db.py
```

Start the FastAPI backend:
```powershell
.venv\Scripts\python.exe -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Start the frontend:
```powershell
cd frontend
copy .env.example .env
npm install
npm run dev
```

## API Endpoints (Current)
- `GET /healthz`
- `POST /workflows/email-operations/run`
- `GET /workflows/runs`
- `GET /approvals/pending`
- `POST /approvals/{approval_id}/decision`

## Inbox and Calendar Connectors
The personal assistant backend can now fetch real inbox and calendar data when configured.

- `INBOX_CONNECTOR=gmail` uses `GOOGLE_ACCESS_TOKEN` against Gmail.
- `CALENDAR_CONNECTOR=google_calendar` uses `GOOGLE_ACCESS_TOKEN` against Google Calendar.
- `INBOX_CONNECTOR=outlook` or `microsoft_graph` uses `MICROSOFT_GRAPH_ACCESS_TOKEN` against Microsoft 365 mail.
- `CALENDAR_CONNECTOR=outlook` or `microsoft_graph` uses `MICROSOFT_GRAPH_ACCESS_TOKEN` against Microsoft 365 calendar.

Use `PERSONAL_ASSISTANT_ACCOUNT_ID` and `PERSONAL_ASSISTANT_CALENDAR_ID` to target the mailbox/calendar, and keep both connector settings at `null` if you want the previous placeholder behavior.

### Outlook Bootstrap
If you have an Azure app registration for Outlook/Microsoft Graph, set:

- `OUTLOOK_TENANT_ID`
- `OUTLOOK_CLIENT_ID`

Then run:
```powershell
.venv\Scripts\python.exe scripts\microsoft_graph_device_code.py
```

That script starts a Microsoft device-code flow and writes the resulting `MICROSOFT_GRAPH_ACCESS_TOKEN` into `.env` automatically. The Azure app still needs delegated Graph permissions for `Mail.Read` and `Calendars.Read`.

### Read Verification
Once the token is present in `.env`, start the API and read the normalized Outlook data directly:

```powershell
.venv\Scripts\python.exe -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/personal-assistant/context | ConvertTo-Json -Depth 6
```

That endpoint returns connector health plus the current normalized `inbox_messages` and `calendar_events` payloads used by the dashboard.

## Frontend MVP Pages
- Workflow monitor: reads workflow runs and surfaces model usage, confidence, and escalation indicators.
- Approval queue: reads pending approvals and provides a review surface ahead of decision wiring.

## Git Hygiene
- Local secrets, virtual environments, caches, and local database files are intentionally excluded via `.gitignore`.
- Line endings are normalized through `.gitattributes` to keep Windows and GitHub diffs stable.
