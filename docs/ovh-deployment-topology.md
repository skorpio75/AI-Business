<!-- Copyright (c) Dario Pizzolante -->
# OVH Deployment Topology

## Purpose
Define a staged OVH deployment model that starts with Track A only, then scales to Track B as clients arrive, while preserving local-first development parity.

## Deployment Principles
- local development remains the primary coding environment
- Track A is deployed first
- Track B is added gradually per real client mission
- inference may be shared, but tenant state is not
- the same env keys and routing model should work locally and in cloud

## Local-First Development Rule
Recommended workflow:

1. code locally
2. run API, frontend, PostgreSQL, and `Ollama` locally
3. commit and push to Git
4. merge in Git
5. cloud instances pull approved changes

Do not rely on cloud-only config logic that cannot be exercised locally first.

## Target Stages

### Stage 0: Local Development
- single repo clone
- local PostgreSQL
- local Track A runtime
- optional local Track B seeded tenants
- local `Ollama`

### Stage 1: Track A First Production
- one Track A app stack
- one Track A database
- one Track A internal `Ollama` path
- cloud fallback enabled through `ModelGateway`

### Stage 2: First Track B Tenant
- keep Track A running
- add one isolated Track B tenant app stack
- add one tenant database
- use shared Track B `Ollama` or cloud fallback

### Stage 3: Track B Scale-Out
- more tenant stacks
- object storage for artifacts and exports
- private networking
- optional shared Track B inference service
- stronger observability and backup posture

## Recommended OVH Shape
These are practical starting shapes, not hard requirements.

### Track A First
| Layer | Local | OVH Starting Shape | Notes |
|---|---|---|---|
| Frontend | Vite dev server | same app node or static reverse-proxy host | keep one codebase |
| API | local Python/uvicorn | one OVH VPS app node | start simple |
| DB | local Postgres + pgvector | OVH Managed PostgreSQL or self-managed Postgres | keep `pgvector` |
| Storage | local files | local volume first, object storage later | migration path matters |
| Inference | local `Ollama` | Track A internal `Ollama` on same box or adjacent box | compact models first |
| Cloud fallback | optional | enabled through `ModelGateway` | for overflow and richer tasks |

### Track B First Client
| Layer | Local | OVH Starting Shape | Notes |
|---|---|---|---|
| App/API | local seeded tenant | one isolated tenant node | per-tenant config and runtime |
| DB | local seeded tenant DB | managed or self-managed Postgres per tenant | keep tenant isolation |
| Storage | local tenant folders | tenant-scoped volume or object-storage prefix | never share tenant roots |
| Inference | local `Ollama` or shared local test endpoint | shared Track B `Ollama` or cloud fallback | inference may be shared |
| Observability | local logs and optional Langfuse | tenant-aware tracing and logs | keep tenant metadata |

## Suggested OVH Service Matrix
These product classes are based on OVH official product lines as of 2026-03-17.

| Need | Recommended OVH Class | Use |
|---|---|---|
| Track A starter app | VPS | first production subscription |
| Track A larger app or split inference | Public Cloud instance or larger VPS | more headroom |
| PostgreSQL | Managed Databases for PostgreSQL where suitable | simpler ops |
| Artifact storage | Object Storage | documents, exports, backups |
| Shared Track B inference | Public Cloud compute, optionally GPU-backed later | shared `Ollama` service |
| Private traffic | vRack/private network where applicable | app to DB and inference |

## Environment and Config Matrix

### Common Keys
| Key | Local Track A | OVH Track A | OVH Track B |
|---|---|---|---|
| `ENV` | `local` | `production` | `production` |
| `PRIMARY_TRACK` | `track_a_internal` | `track_a_internal` | `track_b_client` |
| `TENANT_ID` | `internal` | `internal` | `<tenant>` |
| `DATABASE_URL` | local DB | Track A DB | tenant DB |
| `OLLAMA_BASE_URL` | local ollama | Track A internal ollama | shared Track B or tenant-specific |
| `LOCAL_MODEL` | compact local model | compact local model | compact or shared inference model |
| `CLOUD_MODEL` | optional | enabled | enabled |
| `MODEL_TIMEOUT_SECONDS` | dev-tuned | production-tuned | production-tuned |
| `RUNTIME_ENV_FILE` | root `.env` or local tenant env | Track A env path | tenant env path |

### Track A Internal Inference
- preferred for dogfooding, delivery lab, and prompt iteration
- compact models first
- can later move to a dedicated Track A inference node

### Track B Shared Inference
- one shared `Ollama` server for multiple client runtimes
- no shared tenant DB, storage, or retrieval
- good cost step before dedicated inference per premium client

## Local and Cloud Deployment Workflow
- local is the primary developer environment
- Git is the transport between local and cloud
- cloud pulls merged changes
- schema migrations should be run in each target environment after pull
- cloud should not become the place where code is edited manually

## Migration Guidance
- start with Track A on one small production stack
- keep Track B in template mode until first approved mission
- introduce shared Track B inference only when multiple client runtimes justify it
- move storage to object storage before artifact growth becomes painful

## Concrete Starter Pack
The repo now includes a concrete single-box Track A deployment pack in `deploy/track-a-vps/`, including:

- a VPS-ready compose stack
- a production env template
- a deployment runbook

Use that pack when you want the practical first OVH implementation of the Stage 1 Track A-first shape documented here.

## Official OVH References
- VPS: https://www.ovhcloud.com/en/vps/
- Managed PostgreSQL: https://www.ovhcloud.com/en/public-cloud/postgresql/
- Object Storage: https://support.us.ovhcloud.com/hc/en-us/articles/4603838122643-Getting-started-with-Object-Storage
- GPU overview: https://www.ovhcloud.com/en/public-cloud/gpu/
