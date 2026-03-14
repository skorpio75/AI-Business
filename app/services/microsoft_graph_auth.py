import json
import os
from pathlib import Path
from typing import Any
from urllib import error, parse, request

from app.core.settings import Settings

ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env"
OUTLOOK_PROVIDERS = {"microsoft_graph", "graph", "outlook"}


class MicrosoftGraphAuthError(RuntimeError):
    pass


def outlook_connectors_enabled(settings: Settings) -> bool:
    return (
        settings.inbox_connector.strip().lower() in OUTLOOK_PROVIDERS
        or settings.calendar_connector.strip().lower() in OUTLOOK_PROVIDERS
    )


def post_form(url: str, data: dict[str, str], *, allow_error_payload: bool = False) -> dict[str, Any]:
    payload = parse.urlencode(data).encode("utf-8")
    req = request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=15) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return json.loads(response.read().decode(charset))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        if allow_error_payload:
            try:
                return json.loads(detail)
            except json.JSONDecodeError:
                pass
        raise MicrosoftGraphAuthError(f"Request failed with status {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise MicrosoftGraphAuthError(f"Request failed: {exc.reason}") from exc


def rewrite_env_values(path: Path, values: dict[str, str]) -> None:
    if not path.exists():
        raise MicrosoftGraphAuthError(f"Cannot write token because {path} does not exist.")
    lines = path.read_text(encoding="utf-8").splitlines()
    pending = dict(values)
    for index, line in enumerate(lines):
        for key, value in list(pending.items()):
            if line.startswith(f"{key}="):
                lines[index] = f"{key}={value}"
                pending.pop(key)
                break
    for key, value in pending.items():
        lines.append(f"{key}={value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def persist_tokens(token_payload: dict[str, Any], *, env_path: Path = ENV_PATH) -> None:
    values: dict[str, str] = {}
    access_token = token_payload.get("access_token")
    refresh_token = token_payload.get("refresh_token")
    if access_token:
        token_value = str(access_token)
        os.environ["MICROSOFT_GRAPH_ACCESS_TOKEN"] = token_value
        values["MICROSOFT_GRAPH_ACCESS_TOKEN"] = token_value
    if refresh_token:
        refresh_value = str(refresh_token)
        os.environ["MICROSOFT_GRAPH_REFRESH_TOKEN"] = refresh_value
        values["MICROSOFT_GRAPH_REFRESH_TOKEN"] = refresh_value
    if values:
        rewrite_env_values(env_path, values)


def refresh_access_token(settings: Settings, *, env_path: Path = ENV_PATH) -> dict[str, Any]:
    if not settings.outlook_tenant_id or not settings.outlook_client_id:
        raise MicrosoftGraphAuthError("Missing OUTLOOK_TENANT_ID or OUTLOOK_CLIENT_ID.")
    if not settings.microsoft_graph_refresh_token:
        raise MicrosoftGraphAuthError("Missing MICROSOFT_GRAPH_REFRESH_TOKEN.")

    token_url = f"https://login.microsoftonline.com/{settings.outlook_tenant_id}/oauth2/v2.0/token"
    token_payload = post_form(
        token_url,
        {
            "grant_type": "refresh_token",
            "client_id": settings.outlook_client_id,
            "refresh_token": settings.microsoft_graph_refresh_token,
            "scope": settings.outlook_graph_scopes,
        },
    )
    if "access_token" not in token_payload:
        raise MicrosoftGraphAuthError("Refresh-token response did not include an access token.")

    persist_tokens(token_payload, env_path=env_path)
    return token_payload
