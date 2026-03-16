# Enterprise Agent Platform

## Overview
This project is a reproducible, privacy-isolated enterprise agent platform designed for two parallel goals:

- Track A - Internal Instance: operate a freelance/consulting business with AI-assisted workflows and one human approver.
- Track B - Client Instance Template: deploy isolated, reusable agent-platform instances for end customers without rebuilding from scratch.

The platform is not shared across clients. Each instance is deployed separately for privacy, compliance, and operational clarity.

## Current Status
The committed codebase is still backend-led. It includes the FastAPI API, workflow orchestration and database layer for the initial email-operations slice, plus a `frontend/` React mission-control scaffold with workflow monitoring, approval handling, explicit model-routing visibility, personal assistant summary fed by configurable inbox/calendar connectors, dedicated CTO/CIO, finance, and Chief AI / Digital Strategy specialist panels, and typed consulting-style advisory-analysis endpoints that now run through the governed prompt/model layer for both internal specialist counsel and client-specific consulting work.

## Principles
- open source first
- isolated deployment per company
- markdown-first documentation
- deterministic workflows with AI inside key steps
- one human approval layer for sensitive actions
- reusable templates for agents and workflows
- minimal MVP, scalable architecture later

## Governed Agentic Company Principle
This platform is intended to support a strongly agentic company, but not an ungoverned one.

- LLM capacity should be used as much as possible for reasoning, counseling, consulting, synthesis, drafting, and deliverable preparation.
- Governance remains mandatory around that reasoning through workflows, approval policy, tool boundaries, output schemas, tenancy isolation, routing visibility, and auditability.
- The target model is not rule-only automation and not unconstrained autonomy. It is LLM-first reasoning inside explicit business guardrails.
- Agents may become more autonomous over time, but only through governed runtime promotion, never by bypassing policy or human approval for sensitive actions.

## Operating Modes
The platform currently distinguishes three practical operating modes:

- Internal counseling: internal agents help run the company itself. They use LLM-backed reasoning for strategy, counseling, synthesis, and internal decision support, but remain inside workflow, approval, tool, and audit guardrails.
- Client-facing consulting: client-scoped agents act like consultants on a bounded engagement. They analyze a client brief, frame the mission, recommend relevant services, and surface responsible growth opportunities, but they do so as isolated client instances rather than shared internal agents.
- Future multi-agent runtime: richer multi-agent collaboration is a roadmap direction, not the current control model. As it arrives, it will remain workflow-first, policy-bound, observable, and approval-safe rather than becoming an unconstrained peer-agent mesh.

In short: internal and client-facing agents already use the same governed LLM-first reasoning model, but full multi-agent company behavior is still being introduced in phased, controlled steps.

## Main Tech Components
- FastAPI
- LangGraph
- LiteLLM
- Ollama
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

## Track B Template Pack
The first Track B deployment pack now lives in `config/client-template/`. It includes the starter `client.yaml`, a client-scoped `deployment.env.example`, a `docker-compose.client.yaml` overlay, and a `storage-map.yaml` placeholder for isolated documents, logs, exports, prompt overrides, and connector secrets.

This pack makes the template clonable without changing the shared codebase while keeping later tasks separate for final client-contract design, seeding, runtime isolation hardening, workflow portability checks, and the bootstrap runbook.

## Repository Structure
```text
enterprise-agent-platform/
|- README.md
|- ROADMAP.md
|- EPICS.md
|- ARCHITECTURE.md
|- AGENTS.md
|- AGENT_LLM_ROUTING_MATRIX.md
|- PROMPTS.md
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

## Documentation Rule
- Keep markdown governance files aligned as part of every material change.
- `ROADMAP.md` is the status source of truth and `TODO.md` is the short execution view derived from it.
- `AGENT_LLM_ROUTING_MATRIX.md` is the family-level planning map for compact direct-Ollama, guarded local drafting, richer governed gateway reasoning, and deterministic/hybrid execution posture.
- When architecture, integrations, workflow scope, or implementation status changes, update the affected markdown files in the same change.

## MVP Slice 1 (Working)
- Use case: inbox triage + draft reply + CEO approval.
- Backend: FastAPI endpoint for `email-operations`.
- Model routing: local-first (Ollama), optional cloud fallback (OpenRouter-compatible via LiteLLM).
- Runtime timeout: model requests use `MODEL_TIMEOUT_SECONDS`, configurable through `.env`.

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

Daily startup shortcut:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\dev_start.ps1
```
This script starts Docker, initializes the database, creates `frontend\.env` from `frontend\.env.example` if needed, installs frontend dependencies on first run, and opens separate backend/frontend PowerShell windows.

## API Endpoints (Current)
- `GET /healthz`
- `GET /connectors/bootstrap-status`
- `GET /specialists/cto-cio/panel`
- `POST /specialists/cto-cio/analyze`
- `GET /specialists/finance/panel`
- `GET /specialists/chief-ai-digital-strategy/panel`
- `POST /specialists/chief-ai-digital-strategy/analyze`
- `POST /workflows/email-operations/run`
- `GET /workflows/runs`
- `GET /approvals/pending`
- `POST /approvals/{approval_id}/decision`

## Specialist Advisory Analysis
Client-facing advisory specialists can now analyze a bounded client brief instead of only returning generic panel summaries.

- `POST /specialists/cto-cio/analyze` accepts a problem statement, client context/history, current stack, constraints, and desired outcomes, then returns a consulting mission assessment, context signals, recommended services, upsell opportunities, strategy options, and architecture advice.
- `POST /specialists/chief-ai-digital-strategy/analyze` accepts a problem statement, business/client context, history, process areas, data assets, and delivery constraints, then returns a consulting mission assessment, context signals, recommended services, upsell opportunities, an opportunity map, a phased blueprint, and maturity guidance.
- both specialist analysis endpoints now run through the shared prompt/model layer and return provider/model routing metadata, while deterministic fallback remains in place for resilience and governance-safe output recovery
- the internal CTO/CIO and Chief AI specialist panels also run through the same governed prompt/model layer, now surface provider/model routing metadata in Mission Control, and are assembled from smaller section-level model calls that use compact example-shaped prompts plus a fast local-model override to keep Ollama viable on smaller machines

## Current Control Layers
- normalized events, approval classes, and autonomy classes are defined in backend contracts/config
- state ownership and persistence mapping is defined for `opportunity_state`, `project_state`, `run_state`, and `approval_state`
- normalized tool permission profiles are bound by agent family and operating mode
- runtime prompt composition contracts now define family-base prompt assets, workflow-step prompt assets, and injected operating context rules
- prompt asset naming, storage, and loading conventions are defined, with legacy explicit-path compatibility during migration

## Inbox and Calendar Connectors
The personal assistant backend can now fetch real inbox and calendar data when configured.

- `INBOX_CONNECTOR=gmail` uses `GOOGLE_ACCESS_TOKEN` against Gmail.
- `CALENDAR_CONNECTOR=google_calendar` uses `GOOGLE_ACCESS_TOKEN` against Google Calendar.
- `INBOX_CONNECTOR=outlook` or `microsoft_graph` uses `MICROSOFT_GRAPH_ACCESS_TOKEN` against Microsoft 365 mail.
- `CALENDAR_CONNECTOR=outlook` or `microsoft_graph` uses `MICROSOFT_GRAPH_ACCESS_TOKEN` against Microsoft 365 calendar.
- If `GOOGLE_REFRESH_TOKEN` is configured together with `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`, the backend refreshes the Google access token automatically when building connector context.
- If `MICROSOFT_GRAPH_REFRESH_TOKEN` is configured, the backend refreshes the Microsoft Graph access token automatically each time the API starts and when connector context is rebuilt.
- Provider credentials can live either directly in `.env` or in JSON secret files referenced by `GOOGLE_SECRETS_PATH` and `MICROSOFT_GRAPH_SECRETS_PATH`.

Use `PERSONAL_ASSISTANT_ACCOUNT_ID` and `PERSONAL_ASSISTANT_CALENDAR_ID` to target the mailbox/calendar, and keep both connector settings at `null` if you want the previous placeholder behavior.

### Connector Bootstrap Status
Check the current provider bootstrap state directly from the API:

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/connectors/bootstrap-status | ConvertTo-Json -Depth 6
```

That endpoint reports whether Google and Microsoft Graph are selected, whether access and refresh tokens are present, whether client credentials are present, whether refresh is supported, and whether a secret-store path is configured.

### Google Bootstrap
For Gmail and Google Calendar, set:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- optional `GOOGLE_SECRETS_PATH` if you prefer JSON-file secret storage over `.env`

Then run:

```powershell
.venv\Scripts\python.exe scripts\google_oauth_local_server.py
```

That script opens a Google OAuth authorization URL against the local loopback redirect defined by `GOOGLE_OAUTH_REDIRECT_URI`, exchanges the returned code for tokens, and writes `GOOGLE_ACCESS_TOKEN` plus `GOOGLE_REFRESH_TOKEN` into `.env` or the configured secret store.

### Outlook Bootstrap
If you have an Azure app registration for Outlook/Microsoft Graph, set:

- `OUTLOOK_TENANT_ID`
- `OUTLOOK_CLIENT_ID`
- optional `OUTLOOK_CLIENT_SECRET` if your app registration uses a confidential client
- optional `MICROSOFT_GRAPH_SECRETS_PATH` if you prefer JSON-file secret storage over `.env`

Then run:
```powershell
.venv\Scripts\python.exe scripts\microsoft_graph_device_code.py
```

That script starts a Microsoft device-code flow and writes the resulting `MICROSOFT_GRAPH_ACCESS_TOKEN` and `MICROSOFT_GRAPH_REFRESH_TOKEN` into `.env` automatically. After that initial bootstrap, backend startup refreshes the access token automatically. The Azure app still needs delegated Graph permissions for `Mail.Read` and `Calendars.Read`.

### Outlook Send Approval Flow
Inbox-derived email workflows now carry the source Outlook message ID through the approval queue. When a CEO approves such an item, the backend sends the reply through Microsoft Graph using the source message reply endpoint.

For that full cycle, the Azure app needs:

- `Mail.Read`
- `Calendars.Read`
- `Mail.Send`

### Read Verification
Once the token is present in `.env`, start the API and read the normalized Outlook data directly:

```powershell
.venv\Scripts\python.exe -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/personal-assistant/context | ConvertTo-Json -Depth 6
```

That endpoint returns connector health plus the current normalized `inbox_messages` and `calendar_events` payloads used by the dashboard.

### End-to-End Operator Flow
1. Open the new `Inbox and Calendar` mission-control view.
2. Refresh live Outlook context and select a real inbox message.
3. Launch a draft reply workflow from that message.
4. Review the generated draft in `Approval Queue`.
5. Edit the draft if needed and keep it pending, or approve it to send through Outlook.

## Frontend MVP Pages
- Workflow monitor: reads workflow runs and surfaces model usage, confidence, and escalation indicators.
- Approval queue: reads pending approvals and provides a review surface ahead of decision wiring.
- CTO/CIO panel: packages technology strategy options, architecture advice, and internal platform improvements into one specialist advisory view.
- Finance cockpit: packages accounting exceptions, close readiness, and CFO scenario cards into one finance review surface.
- Chief AI / Digital Strategy: packages AI opportunity maps, delivery blueprinting, and maturity signals into one strategy surface.

The advisory panels remain useful operator summaries, while the specialist analysis endpoints are the path for client-specific consulting output based on a problem statement and engagement context/history. Those outputs now also help the consulting company grow by surfacing adjacent, relevant follow-on opportunities for the same client.

## Git Hygiene
- Local secrets, virtual environments, caches, and local database files are intentionally excluded via `.gitignore`.
- Line endings are normalized through `.gitattributes` to keep Windows and GitHub diffs stable.
