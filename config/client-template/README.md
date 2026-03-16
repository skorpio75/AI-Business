<!-- Copyright (c) Dario Pizzolante -->
# Track B Client Template Pack

This folder is the first reusable deployment pack for Track B client instances.

It packages the minimum artifacts needed to clone a client-scoped deployment without reworking the shared codebase:

- `client.yaml`: finalized Track B client contract covering tenant identity, governance, deployment, storage, connectors, model routing, and default workflow/service packaging.
- `deployment.env.example`: client-scoped environment template for ports, database naming, tenant identity, and secret-store paths.
- `docker-compose.client.yaml`: compose overlay that gives a cloned client deployment its own PostgreSQL container identity and named volume.
- `storage-map.yaml`: canonical placeholder paths for client documents, logs, exports, prompt overrides, and connector secrets.

The pack is designed to preserve the Track A / Track B isolation rule:

- shared codebase and workflow templates
- isolated tenant identity
- isolated database naming and port assignment
- isolated secret-store paths
- isolated storage roots for documents, logs, and exports
- isolated runtime env file used for token persistence and connector bootstrap updates

Example composition:

```powershell
docker compose -f docker-compose.yml -f config/client-template/docker-compose.client.yaml --env-file config/client-template/deployment.env.example up -d
```

`P4-T04` now enforces the storage and credential boundary in runtime settings: Track B instances require a client-scoped `RUNTIME_ENV_FILE`, storage roots must stay under `data/clients/<tenant>/`, prompt overrides under `prompts/clients/<tenant>/`, and connector secrets under `secrets/<tenant>/`.

`P4-T03` now provides `scripts/seed_config.py`, which turns this template pack into a tenant-specific client contract and runtime env file under `config/clients/` and creates the tenant directory roots expected by the runtime.

`P4-T05` now validates portability across seeded client instances: `knowledge-qna` and `email-operations` run under tenant-scoped runtime settings, while `document-intake` and `reporting` remain governed workflow-pack entries pending service implementation.

`P4-T06` is now captured in `docs/track-b-bootstrap-runbook.md`, which documents the tenant seed flow, the `RUNTIME_ENV_FILE` activation rule, database and API startup, connector bootstrap, verification, and cleanup steps for a real client instance.

The client env template now also carries optional Langfuse settings so workflow/model tracing can be enabled per client instance without changing shared code.
