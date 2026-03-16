# Track B Bootstrap Runbook

## Purpose
Use this runbook to create and start a tenant-isolated Track B client instance from the shared template pack without falling back to Track A defaults.

## Scope
This runbook covers:

- seeding a tenant-specific client contract and runtime env file
- starting isolated PostgreSQL with the Track B compose overlay
- running database migrations and the API against the tenant env
- bootstrapping Google or Microsoft connector tokens into the tenant-scoped env or secret store
- verifying the seeded instance with the currently portable workflows

This runbook does not claim that every Track B workflow is executable today. `knowledge-qna` and `email-operations` are the validated reusable services. `document-intake` and `reporting` remain governed workflow-pack contract entries pending service implementation.

## Operator Rule
Set `RUNTIME_ENV_FILE` in the shell before running any Python command for a Track B client instance.

Why this matters:

- `app.core.settings` resolves the active env file from `RUNTIME_ENV_FILE`
- `scripts/init_db.py`, `uvicorn`, `scripts/google_oauth_local_server.py`, and `scripts/microsoft_graph_device_code.py` all load settings at process start
- if `RUNTIME_ENV_FILE` is missing, the process can fall back to the shared root `.env`, which breaks Track B isolation

## Prerequisites
- Python virtual environment created at `.venv`
- dependencies installed with `pip install -r requirements.txt`
- Docker Desktop or another local Docker runtime available
- optional: Ollama running locally if you want local-model-backed workflow behavior
- optional: Google or Azure app registration ready if you want live inbox/calendar connectors

## 1. Seed The Client Instance
Run the seed script from the repo root:

```powershell
.\.venv\Scripts\python.exe scripts\seed_config.py --client-id acme-erp-rollout --name "Acme ERP Rollout" --tenant-id acme-erp --api-port 8010 --postgres-port 5450
```

Expected outputs:

- `config/clients/acme-erp.yaml`
- `config/clients/acme-erp.env`
- `data/clients/acme-erp/`
- `prompts/clients/acme-erp/`
- `secrets/acme-erp/`

Use `--dry-run` to preview outputs and `--force` only when you intentionally want to overwrite an existing generated client contract or env file.

## 2. Review The Generated Tenant Files
Check these generated files before startup:

- `config/clients/<tenant>.yaml`
- `config/clients/<tenant>.env`

Confirm that:

- `PRIMARY_TRACK=track_b_client`
- `TENANT_ID=<tenant>`
- `RUNTIME_ENV_FILE=config/clients/<tenant>.env`
- `DATABASE_URL` points at the tenant PostgreSQL port and database
- `CLIENT_DOCUMENTS_DIR`, `CLIENT_LOGS_DIR`, `CLIENT_EXPORTS_DIR`, `CLIENT_VECTOR_DIR`, and `CLIENT_PROMPT_OVERRIDE_DIR` all point inside the tenant roots
- `GOOGLE_SECRETS_PATH` and `MICROSOFT_GRAPH_SECRETS_PATH` point inside `secrets/<tenant>/`

Do not edit `config/client-template/` for a live client. Treat that folder as the shared blueprint and `config/clients/` as the generated tenant runtime config.

## 3. Activate The Tenant Runtime Env In Your Shell
In the same PowerShell session you will use for migrations, API startup, and connector bootstrap:

```powershell
$env:RUNTIME_ENV_FILE = "config/clients/acme-erp.env"
```

Recommended sanity check:

```powershell
Write-Output $env:RUNTIME_ENV_FILE
Get-Content $env:RUNTIME_ENV_FILE
```

If you open a new terminal window, set `RUNTIME_ENV_FILE` again there before running Python commands.

## 4. Start Isolated PostgreSQL
Start the tenant database using the shared base compose file plus the Track B overlay, with the generated tenant env file:

```powershell
docker compose -f docker-compose.yml -f config/client-template/docker-compose.client.yaml --env-file config/clients/acme-erp.env up -d postgres
```

This gives the client instance:

- its own PostgreSQL container name
- its own database name and port
- its own named Docker volume

## 5. Apply Database Migrations
With `RUNTIME_ENV_FILE` already set in the shell:

```powershell
.\.venv\Scripts\python.exe scripts\init_db.py
```

This uses the tenant `DATABASE_URL` from `config/clients/<tenant>.env`.

## 6. Start The API Against The Tenant Env
Still in a shell that has `RUNTIME_ENV_FILE` set:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --host 0.0.0.0 --port 8010 --reload
```

Use the tenant API port from the generated env file if you changed it during seeding.

At startup the app will:

- validate Track B isolation rules
- create tenant-scoped runtime directories if needed
- attempt provider token bootstrap against the active tenant env or tenant secret store

## 7. Verify Runtime Health And Bootstrap State
From a second shell:

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8010/healthz | ConvertTo-Json -Depth 6
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8010/connectors/bootstrap-status | ConvertTo-Json -Depth 6
```

Look for:

- the tenant app responding on the expected port
- connector status reflecting the active tenant env values rather than shared root `.env` values

## 8. Optional Connector Bootstrap
Run these only after setting `RUNTIME_ENV_FILE` for the tenant shell.

### Google
Populate these values in `config/clients/<tenant>.env` or the tenant secret store path:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- optional `GOOGLE_SECRETS_PATH`

Then run:

```powershell
.\.venv\Scripts\python.exe scripts\google_oauth_local_server.py
```

The script writes `GOOGLE_ACCESS_TOKEN` and `GOOGLE_REFRESH_TOKEN` to the active runtime env file or configured tenant secret store.

### Microsoft Graph
Populate these values in `config/clients/<tenant>.env` or the tenant secret store path:

- `OUTLOOK_TENANT_ID`
- `OUTLOOK_CLIENT_ID`
- optional `OUTLOOK_CLIENT_SECRET`
- optional `MICROSOFT_GRAPH_SECRETS_PATH`

Then run:

```powershell
.\.venv\Scripts\python.exe scripts\microsoft_graph_device_code.py
```

The script writes `MICROSOFT_GRAPH_ACCESS_TOKEN` and `MICROSOFT_GRAPH_REFRESH_TOKEN` to the active runtime env file or configured tenant secret store.

## 9. Smoke Test The Portable Workflows
### Knowledge Q&A
Place at least one `.md` or `.txt` file under `data/clients/<tenant>/documents`, then call:

```powershell
$body = @{ question = "What does this client instance support?"; limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8010/knowledge/qna -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 6
```

### Email Operations
```powershell
$body = @{
  sender = "client@example.com"
  subject = "Need an update"
  body = "Please confirm the next delivery checkpoint."
  source_account_id = "acme-erp"
  source_message_id = "msg-001"
  source_thread_id = "thread-001"
  source_provider = "microsoft_graph"
} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8010/workflows/email-operations/run -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 6
```

Then confirm:

- `GET /workflows/runs`
- `GET /approvals/pending`

These are the currently validated reusable Track B workflows across seeded instances.

## 10. Shutdown And Cleanup
Stop the tenant database:

```powershell
docker compose -f docker-compose.yml -f config/client-template/docker-compose.client.yaml --env-file config/clients/acme-erp.env down
```

To remove the tenant volume as well:

```powershell
docker compose -f docker-compose.yml -f config/client-template/docker-compose.client.yaml --env-file config/clients/acme-erp.env down -v
```

Use care with cleanup. Removing the Docker volume deletes the tenant database contents for that local instance.

## Troubleshooting
### The app says Track B requires `RUNTIME_ENV_FILE`
Set `RUNTIME_ENV_FILE` in the current shell before running the command again.

### Tokens were written to the wrong place
You likely ran a bootstrap script without the tenant `RUNTIME_ENV_FILE` set, or with a secret path pointing outside `secrets/<tenant>/`.

### The API starts but uses the wrong database or port
Re-open `config/clients/<tenant>.env`, confirm `DATABASE_URL`, `POSTGRES_PORT`, and `API_PORT`, then restart the database and API from a shell with the correct `RUNTIME_ENV_FILE`.

### Knowledge Q&A returns no grounded citations
Add `.md` or `.txt` documents under `data/clients/<tenant>/documents` and retry with a narrower question.

### `document-intake` or `reporting` do not have runnable endpoints
That is expected today. They remain part of the Track B workflow pack contract, but their service implementations are not yet present in the codebase.
