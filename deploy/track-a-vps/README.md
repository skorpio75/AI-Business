# Track A Single-VPS Pack

This pack runs the current internal Track A stack on one VPS:

- `web`: Caddy serving the built frontend and reverse-proxying API routes
- `api`: FastAPI backend
- `postgres`: local PostgreSQL with `pgvector`
- `ollama`: local model runtime

It is intentionally a simple first-production shape. The database is local to the VPS so you can start slowly, then move it off-box later by changing `DATABASE_URL`.

## 1. Prepare The VPS

Recommended host layout:

```text
/opt/ai-business
/opt/ai-business-data
```

Clone the repo into `/opt/ai-business`, then install Docker Engine plus the Docker Compose plugin.

Create the persistence roots:

```bash
sudo mkdir -p /opt/ai-business-data/postgres
sudo mkdir -p /opt/ai-business-data/ollama
sudo mkdir -p /opt/ai-business-data/data/internal
sudo mkdir -p /opt/ai-business-data/prompts/internal
sudo mkdir -p /opt/ai-business-data/secrets/internal
```

## 2. Create The VPS Env File

From the repo root:

```bash
cp deploy/track-a-vps/.env.track-a-vps.example deploy/track-a-vps/.env.track-a-vps
```

Set at least these values:

- `POSTGRES_PASSWORD`
- `PUBLIC_SITE_ADDR`
- `ACME_EMAIL`
- `OPENROUTER_API_KEY` if cloud fallback should be enabled

Use `PUBLIC_SITE_ADDR=:80` for initial IP-only smoke tests.
Use `PUBLIC_SITE_ADDR=your-domain.example.com` once DNS points at the VPS and you want automatic HTTPS.

## 3. Build And Start Core Services

```bash
docker compose --env-file deploy/track-a-vps/.env.track-a-vps -f deploy/track-a-vps/docker-compose.yml up -d postgres ollama
```

Pull the compact local models you want available:

```bash
docker compose --env-file deploy/track-a-vps/.env.track-a-vps -f deploy/track-a-vps/docker-compose.yml exec ollama ollama pull qwen2.5:1.5b-instruct-q4_K_M
docker compose --env-file deploy/track-a-vps/.env.track-a-vps -f deploy/track-a-vps/docker-compose.yml exec ollama ollama pull llama3.2:3b
```

Apply database migrations:

```bash
docker compose --env-file deploy/track-a-vps/.env.track-a-vps -f deploy/track-a-vps/docker-compose.yml --profile ops run --rm db-migrate
```

Start the app:

```bash
docker compose --env-file deploy/track-a-vps/.env.track-a-vps -f deploy/track-a-vps/docker-compose.yml up -d api web
```

## 4. Smoke Test

```bash
docker compose --env-file deploy/track-a-vps/.env.track-a-vps -f deploy/track-a-vps/docker-compose.yml ps
curl http://127.0.0.1/healthz
```

If `PUBLIC_SITE_ADDR` is a real domain, also test:

```bash
curl https://your-domain.example.com/healthz
```

## 5. Day-2 Commands

Tail logs:

```bash
docker compose --env-file deploy/track-a-vps/.env.track-a-vps -f deploy/track-a-vps/docker-compose.yml logs -f api
docker compose --env-file deploy/track-a-vps/.env.track-a-vps -f deploy/track-a-vps/docker-compose.yml logs -f web
```

Restart after a git pull:

```bash
docker compose --env-file deploy/track-a-vps/.env.track-a-vps -f deploy/track-a-vps/docker-compose.yml up -d --build api web
```

## 6. Backup The Local DB

At minimum, run a daily dump:

```bash
docker compose --env-file deploy/track-a-vps/.env.track-a-vps -f deploy/track-a-vps/docker-compose.yml exec -T postgres sh -lc 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > /opt/ai-business-data/postgres/backup-$(date +%F).sql
```

## 7. Later DB Migration

When you are ready to move Postgres off the VPS:

1. provision managed PostgreSQL or a second DB host
2. restore a fresh dump there
3. change `DATABASE_URL` in `deploy/track-a-vps/.env.track-a-vps`
4. rerun `db-migrate`
5. restart `api`

The app container and web container do not need structural changes for that migration.
