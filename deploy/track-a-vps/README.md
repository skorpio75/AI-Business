# Track A Single-VPS Pack

This pack runs the current internal Track A stack on one VPS:

- `web`: Caddy serving the built frontend and reverse-proxying API routes
- `api`: FastAPI backend
- `postgres`: local PostgreSQL with `pgvector`
- `ollama`: local model runtime

It is intentionally a simple first-production shape. The database is local to the VPS so you can start slowly, then move it off-box later by changing `DATABASE_URL`.

## Private GitHub Setup

For a private GitHub repo, the safest simple setup is a read-only deploy key on the VPS.

On the VPS:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t ed25519 -f ~/.ssh/ai-business-deploy -C "ovh-track-a-vps"
cat ~/.ssh/ai-business-deploy.pub
```

Add that public key in GitHub:

- repo `Settings`
- `Deploy keys`
- `Add deploy key`
- read-only access only

Then create `~/.ssh/config`:

```text
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/ai-business-deploy
  IdentitiesOnly yes
```

Lock down the file:

```bash
chmod 600 ~/.ssh/config ~/.ssh/ai-business-deploy
```

Test access:

```bash
ssh -T git@github.com
```

You should see a successful GitHub authentication message without shell access.

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

### Fastest Path: Copy One Script And Let It Clone The Repo

From your local machine, copy the installer script to the VPS:

```bash
scp deploy/track-a-vps/install.sh user@your-vps-ip:/tmp/ai-business-install.sh
ssh user@your-vps-ip
chmod +x /tmp/ai-business-install.sh
```

Then run it on the VPS:

```bash
/tmp/ai-business-install.sh --repo git@github.com:your-org/your-private-repo.git --branch main
```

That script:

- clones or updates the repo to `/opt/ai-business`
- creates `/opt/ai-business-data/...`
- creates `deploy/track-a-vps/.env.track-a-vps` if missing
- starts the stack once the env file is ready

If the env file still has placeholder values, the script stops safely and tells you what to edit.

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

If you already ran `install.sh`, you usually do not need the manual commands below except for troubleshooting or a later redeploy.

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

Or use the installer again for idempotent update plus restart:

```bash
bash /opt/ai-business/deploy/track-a-vps/install.sh --repo git@github.com:your-org/your-private-repo.git --branch main
```

## Troubleshooting

If specialist panels fall back to rules with an Ollama `HTTP 404` diagnostic, the app reached the configured host but that host was not serving the Ollama API route expected at `/api/generate`.

Quick checks:

```bash
docker compose --env-file deploy/track-a-vps/.env.track-a-vps -f deploy/track-a-vps/docker-compose.yml ps
docker compose --env-file deploy/track-a-vps/.env.track-a-vps -f deploy/track-a-vps/docker-compose.yml exec ollama ollama list
docker compose --env-file deploy/track-a-vps/.env.track-a-vps -f deploy/track-a-vps/docker-compose.yml exec api python -c "from urllib.request import urlopen; print(urlopen('http://ollama:11434/api/tags').read().decode())"
```

If the last command fails or returns something other than Ollama JSON, verify that:

- `OLLAMA_BASE_URL` still points to the Ollama service
- the `ollama` container is running in the same compose project
- no reverse proxy or platform service is answering on that hostname instead
- `OPENROUTER_API_KEY` is set if you want cloud fallback available when local Ollama is unavailable

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
