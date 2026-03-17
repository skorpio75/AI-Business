#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  install.sh --repo <git_repo_url> [--branch <branch>] [--app-dir <path>] [--data-root <path>] [--skip-start] [--no-model-pull]

Examples:
  ./install.sh --repo git@github.com:your-org/ai-business.git --branch main
  ./install.sh --repo git@github.com:your-org/ai-business.git --app-dir /opt/ai-business --data-root /opt/ai-business-data

What it does:
  - clones or updates the repo on the VPS
  - creates the Track A persistence directories
  - creates deploy/track-a-vps/.env.track-a-vps from the example if missing
  - optionally starts postgres, ollama, migrations, api, and web

Notes:
  - install Docker Engine, Docker Compose plugin, and git first
  - for private GitHub repos, configure SSH deploy-key access before running this script
EOF
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

ensure_env_line() {
  local file_path="$1"
  local key="$2"
  local value="$3"

  if grep -q "^${key}=" "$file_path"; then
    sed -i "s|^${key}=.*|${key}=${value}|" "$file_path"
  else
    printf '\n%s=%s\n' "$key" "$value" >>"$file_path"
  fi
}

wait_for_ollama() {
  local compose_file="$1"
  local env_file="$2"
  local attempt

  for attempt in $(seq 1 30); do
    if docker compose --env-file "$env_file" -f "$compose_file" exec -T ollama ollama list >/dev/null 2>&1; then
      return 0
    fi
    sleep 2
  done

  echo "Ollama did not become ready in time." >&2
  exit 1
}

pull_model_if_set() {
  local compose_file="$1"
  local env_file="$2"
  local model_name="$3"

  if [[ -n "$model_name" ]]; then
    docker compose --env-file "$env_file" -f "$compose_file" exec -T ollama ollama pull "$model_name"
  fi
}

REPO_URL=""
BRANCH="main"
APP_DIR="/opt/ai-business"
DATA_ROOT="/opt/ai-business-data"
START_STACK="true"
PULL_MODELS="true"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      REPO_URL="${2:-}"
      shift 2
      ;;
    --branch)
      BRANCH="${2:-}"
      shift 2
      ;;
    --app-dir)
      APP_DIR="${2:-}"
      shift 2
      ;;
    --data-root)
      DATA_ROOT="${2:-}"
      shift 2
      ;;
    --skip-start)
      START_STACK="false"
      shift
      ;;
    --no-model-pull)
      PULL_MODELS="false"
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$REPO_URL" ]]; then
  echo "--repo is required." >&2
  usage
  exit 1
fi

require_command git
require_command docker

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose plugin is required." >&2
  exit 1
fi

mkdir -p "$DATA_ROOT/postgres"
mkdir -p "$DATA_ROOT/ollama"
mkdir -p "$DATA_ROOT/data/internal"
mkdir -p "$DATA_ROOT/prompts/internal"
mkdir -p "$DATA_ROOT/secrets/internal"

if [[ -d "$APP_DIR" && ! -d "$APP_DIR/.git" ]]; then
  if [[ -n "$(ls -A "$APP_DIR")" ]]; then
    echo "App directory exists but is not a git checkout: $APP_DIR" >&2
    echo "Choose a different --app-dir or clean that directory first." >&2
    exit 1
  fi
fi

if [[ -d "$APP_DIR/.git" ]]; then
  git -C "$APP_DIR" fetch --all --prune
  git -C "$APP_DIR" checkout "$BRANCH"
  git -C "$APP_DIR" pull --ff-only origin "$BRANCH"
else
  git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
fi

ENV_EXAMPLE="$APP_DIR/deploy/track-a-vps/.env.track-a-vps.example"
ENV_FILE="$APP_DIR/deploy/track-a-vps/.env.track-a-vps"
COMPOSE_FILE="$APP_DIR/deploy/track-a-vps/docker-compose.yml"

if [[ ! -f "$ENV_FILE" ]]; then
  cp "$ENV_EXAMPLE" "$ENV_FILE"
fi

ensure_env_line "$ENV_FILE" "TRACK_A_DATA_ROOT" "$DATA_ROOT"

if grep -q '^POSTGRES_PASSWORD=change-this-now$' "$ENV_FILE"; then
  cat <<EOF
Track A env file created at:
  $ENV_FILE

Edit that file before starting the stack.
Minimum values to change:
  POSTGRES_PASSWORD
  PUBLIC_SITE_ADDR
  ACME_EMAIL

Then rerun:
  bash $APP_DIR/deploy/track-a-vps/install.sh --repo $REPO_URL --branch $BRANCH --app-dir $APP_DIR --data-root $DATA_ROOT
EOF
  exit 0
fi

if [[ "$START_STACK" != "true" ]]; then
  echo "Repo prepared and env file is ready at $ENV_FILE"
  exit 0
fi

docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d postgres ollama
wait_for_ollama "$COMPOSE_FILE" "$ENV_FILE"

if [[ "$PULL_MODELS" == "true" ]]; then
  LOCAL_MODEL="$(grep '^LOCAL_MODEL=' "$ENV_FILE" | cut -d= -f2- || true)"
  EMAIL_LOCAL_MODEL="$(grep '^EMAIL_LOCAL_MODEL=' "$ENV_FILE" | cut -d= -f2- || true)"
  EMAIL_STRONG_LOCAL_MODEL="$(grep '^EMAIL_STRONG_LOCAL_MODEL=' "$ENV_FILE" | cut -d= -f2- || true)"

  pull_model_if_set "$COMPOSE_FILE" "$ENV_FILE" "$LOCAL_MODEL"
  if [[ "$EMAIL_LOCAL_MODEL" != "$LOCAL_MODEL" ]]; then
    pull_model_if_set "$COMPOSE_FILE" "$ENV_FILE" "$EMAIL_LOCAL_MODEL"
  fi
  if [[ "$EMAIL_STRONG_LOCAL_MODEL" != "$LOCAL_MODEL" && "$EMAIL_STRONG_LOCAL_MODEL" != "$EMAIL_LOCAL_MODEL" ]]; then
    pull_model_if_set "$COMPOSE_FILE" "$ENV_FILE" "$EMAIL_STRONG_LOCAL_MODEL"
  fi
fi

docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" --profile ops run --rm db-migrate
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d api web

cat <<EOF
Track A VPS stack is up.

Useful commands:
  docker compose --env-file $ENV_FILE -f $COMPOSE_FILE ps
  docker compose --env-file $ENV_FILE -f $COMPOSE_FILE logs -f api
  curl http://127.0.0.1/healthz
EOF
