import argparse
import copy
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "config" / "client-template"


@dataclass
class SeedResult:
    client_config_path: Path
    runtime_env_path: Path
    created_directories: list[Path]
    client_id: str
    tenant_id: str
    slug: str


def _slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return normalized or "client"


def _database_slug(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()
    return normalized or "client"


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected YAML object in {path}")
    return payload


def _render_env_template(template_text: str, values: dict[str, str]) -> str:
    rendered_lines = []
    for raw_line in template_text.splitlines():
        line = raw_line
        if "=" in raw_line and not raw_line.lstrip().startswith("#"):
            key, _, current = raw_line.partition("=")
            line = f"{key}={values.get(key, current)}"
        rendered_lines.append(line)
    return "\n".join(rendered_lines) + "\n"


def _build_seed_values(
    *,
    client_id: str,
    slug: str,
    tenant_id: str,
    name: str,
    legal_name: str,
    timezone: str,
    locale: str,
    api_port: int,
    postgres_port: int,
) -> dict[str, str]:
    db_slug = _database_slug(slug)
    database_name = f"{db_slug}_platform"
    runtime_env_file = f"config/clients/{tenant_id}.env"
    return {
        "client_id": client_id,
        "slug": slug,
        "tenant_id": tenant_id,
        "name": name,
        "legal_name": legal_name,
        "timezone": timezone,
        "locale": locale,
        "app_name": f"enterprise-agent-platform-{slug}",
        "environment_name": slug,
        "api_port": str(api_port),
        "postgres_port": str(postgres_port),
        "database_name": database_name,
        "runtime_env_file": runtime_env_file,
        "documents_root": f"data/clients/{tenant_id}/documents",
        "logs_root": f"data/clients/{tenant_id}/logs",
        "exports_root": f"data/clients/{tenant_id}/exports",
        "vector_root": f"data/clients/{tenant_id}/vector",
        "prompt_override_root": f"prompts/clients/{tenant_id}",
        "google_secret_path": f"secrets/{tenant_id}/google-oauth.json",
        "microsoft_secret_path": f"secrets/{tenant_id}/microsoft-graph.json",
        "database_url": f"postgresql+psycopg://agent:agent@localhost:{postgres_port}/{database_name}",
    }


def _seed_client_contract(template: dict[str, Any], *, values: dict[str, str]) -> dict[str, Any]:
    seeded = copy.deepcopy(template)
    seeded["client"]["id"] = values["client_id"]
    seeded["client"]["slug"] = values["slug"]
    seeded["client"]["name"] = values["name"]
    seeded["client"]["legal_name"] = values["legal_name"]
    seeded["client"]["timezone"] = values["timezone"]
    seeded["client"]["locale"] = values["locale"]
    seeded["client"]["lifecycle_stage"] = "seeded"

    seeded["tenancy"]["tenant_id"] = values["tenant_id"]
    seeded["deployment"]["environment_name"] = values["environment_name"]
    seeded["deployment"]["app_name"] = values["app_name"]
    seeded["deployment"]["compose"]["env_file"] = values["runtime_env_file"]
    seeded["deployment"]["api"]["port"] = int(values["api_port"])
    seeded["deployment"]["database"]["database_name"] = values["database_name"]
    seeded["deployment"]["database"]["port"] = int(values["postgres_port"])

    seeded["storage"]["documents_root"] = values["documents_root"]
    seeded["storage"]["logs_root"] = values["logs_root"]
    seeded["storage"]["exports_root"] = values["exports_root"]
    seeded["storage"]["vector_root"] = values["vector_root"]
    seeded["storage"]["prompt_override_root"] = values["prompt_override_root"]
    seeded["storage"]["secret_paths"]["google_oauth"] = values["google_secret_path"]
    seeded["storage"]["secret_paths"]["microsoft_graph"] = values["microsoft_secret_path"]

    seeded["notes"] = list(seeded.get("notes", [])) + [
        f"Seeded client instance for tenant `{values['tenant_id']}`.",
        f"Runtime env file: `{values['runtime_env_file']}`.",
    ]
    return seeded


def seed_client_instance(
    *,
    client_id: str,
    name: str,
    output_root: Path = ROOT,
    slug: str | None = None,
    tenant_id: str | None = None,
    legal_name: str | None = None,
    timezone: str | None = None,
    locale: str | None = None,
    api_port: int | None = None,
    postgres_port: int | None = None,
    force: bool = False,
    dry_run: bool = False,
) -> SeedResult:
    template = _load_yaml(TEMPLATE_ROOT / "client.yaml")
    env_template = (TEMPLATE_ROOT / "deployment.env.example").read_text(encoding="utf-8")

    resolved_slug = slug or _slugify(client_id)
    resolved_tenant = tenant_id or resolved_slug
    resolved_legal_name = legal_name or name
    resolved_timezone = timezone or template["client"]["timezone"]
    resolved_locale = locale or template["client"]["locale"]
    resolved_api_port = api_port or int(template["deployment"]["api"]["port"])
    resolved_postgres_port = postgres_port or int(template["deployment"]["database"]["port"])

    values = _build_seed_values(
        client_id=client_id,
        slug=resolved_slug,
        tenant_id=resolved_tenant,
        name=name,
        legal_name=resolved_legal_name,
        timezone=resolved_timezone,
        locale=resolved_locale,
        api_port=resolved_api_port,
        postgres_port=resolved_postgres_port,
    )
    contract = _seed_client_contract(template, values=values)

    clients_dir = output_root / "config" / "clients"
    client_config_path = clients_dir / f"{resolved_tenant}.yaml"
    runtime_env_path = clients_dir / f"{resolved_tenant}.env"
    created_directories = [
        output_root / values["documents_root"],
        output_root / values["logs_root"],
        output_root / values["exports_root"],
        output_root / values["vector_root"],
        output_root / values["prompt_override_root"],
        output_root / f"secrets/{resolved_tenant}",
        clients_dir,
    ]

    if not force:
        for path in (client_config_path, runtime_env_path):
            if path.exists():
                raise FileExistsError(f"{path} already exists. Use --force to overwrite it.")

    if not dry_run:
        for directory in created_directories:
            directory.mkdir(parents=True, exist_ok=True)
        client_config_path.write_text(
            yaml.safe_dump(contract, sort_keys=False, allow_unicode=False),
            encoding="utf-8",
        )
        env_values = {
            "CLIENT_SLUG": values["slug"],
            "CLIENT_NAME": values["name"],
            "TENANT_ID": values["tenant_id"],
            "TRACK": "track_b_client",
            "PRIMARY_TRACK": "track_b_client",
            "RUNTIME_ENV_FILE": values["runtime_env_file"],
            "APP_NAME": values["app_name"],
            "ENV": values["environment_name"],
            "API_PORT": values["api_port"],
            "DATABASE_URL": values["database_url"],
            "POSTGRES_DB": values["database_name"],
            "POSTGRES_PORT": values["postgres_port"],
            "GOOGLE_SECRETS_PATH": values["google_secret_path"],
            "MICROSOFT_GRAPH_SECRETS_PATH": values["microsoft_secret_path"],
            "CLIENT_DOCUMENTS_DIR": values["documents_root"],
            "CLIENT_LOGS_DIR": values["logs_root"],
            "CLIENT_EXPORTS_DIR": values["exports_root"],
            "CLIENT_VECTOR_DIR": values["vector_root"],
            "CLIENT_PROMPT_OVERRIDE_DIR": values["prompt_override_root"],
        }
        runtime_env_path.write_text(_render_env_template(env_template, env_values), encoding="utf-8")

    return SeedResult(
        client_config_path=client_config_path,
        runtime_env_path=runtime_env_path,
        created_directories=created_directories,
        client_id=client_id,
        tenant_id=resolved_tenant,
        slug=resolved_slug,
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Seed a Track B client instance from the template pack.")
    parser.add_argument("--client-id", required=True, help="Stable client contract id, for example acme-erp-rollout")
    parser.add_argument("--name", required=True, help="Display name for the client instance")
    parser.add_argument("--slug", help="URL-safe slug. Defaults to a slugified client id.")
    parser.add_argument("--tenant-id", help="Tenant identifier. Defaults to the resolved slug.")
    parser.add_argument("--legal-name", help="Optional legal name. Defaults to --name.")
    parser.add_argument("--timezone", help="Optional timezone override.")
    parser.add_argument("--locale", help="Optional locale override.")
    parser.add_argument("--api-port", type=int, help="Optional API port override.")
    parser.add_argument("--postgres-port", type=int, help="Optional Postgres port override.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing generated config/env files.")
    parser.add_argument("--dry-run", action="store_true", help="Show the planned outputs without writing files.")
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        result = seed_client_instance(
            client_id=args.client_id,
            name=args.name,
            slug=args.slug,
            tenant_id=args.tenant_id,
            legal_name=args.legal_name,
            timezone=args.timezone,
            locale=args.locale,
            api_port=args.api_port,
            postgres_port=args.postgres_port,
            force=args.force,
            dry_run=args.dry_run,
        )
    except FileExistsError as exc:
        parser.error(str(exc))
        return 2

    mode = "Dry run" if args.dry_run else "Seeded"
    print(f"{mode} client instance `{result.tenant_id}`")
    print(f"Client contract: {result.client_config_path.relative_to(ROOT)}")
    print(f"Runtime env: {result.runtime_env_path.relative_to(ROOT)}")
    print("Directories:")
    for directory in result.created_directories:
        print(f"- {directory.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
