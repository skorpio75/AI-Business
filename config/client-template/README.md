# Track B Client Template Pack

This folder is the first reusable deployment pack for Track B client instances.

It packages the minimum artifacts needed to clone a client-scoped deployment without reworking the shared codebase:

- `client.yaml`: client identity placeholder config. This remains intentionally minimal until `P4-T02`.
- `deployment.env.example`: client-scoped environment template for ports, database naming, tenant identity, and secret-store paths.
- `docker-compose.client.yaml`: compose overlay that gives a cloned client deployment its own PostgreSQL container identity and named volume.
- `storage-map.yaml`: canonical placeholder paths for client documents, logs, exports, prompt overrides, and connector secrets.

The pack is designed to preserve the Track A / Track B isolation rule:

- shared codebase and workflow templates
- isolated tenant identity
- isolated database naming and port assignment
- isolated secret-store paths
- isolated storage roots for documents, logs, and exports

Example composition:

```powershell
docker compose -f docker-compose.yml -f config/client-template/docker-compose.client.yaml --env-file config/client-template/deployment.env.example up -d
```

This pack is the Track B scaffold only. Later tasks still finalize the client contract, build seeding automation, harden runtime storage/credential isolation, validate workflow portability, and document the full bootstrap runbook.
