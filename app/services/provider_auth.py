import json
import logging
import os
from pathlib import Path
from typing import Any, Optional
from urllib import error, parse, request

from app.core.settings import Settings
from app.models.connectors import ConnectorBootstrapStatusResponse, ProviderBootstrapStatus

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env"
OUTLOOK_PROVIDERS = {"microsoft_graph", "graph", "outlook"}
GOOGLE_INBOX_PROVIDERS = {"gmail"}
GOOGLE_CALENDAR_PROVIDERS = {"google", "google_calendar", "google-calendar"}


class ProviderAuthError(RuntimeError):
    pass


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
        raise ProviderAuthError(f"Request failed with status {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise ProviderAuthError(f"Request failed: {exc.reason}") from exc


def outlook_connectors_enabled(settings: Settings) -> bool:
    return (
        settings.inbox_connector.strip().lower() in OUTLOOK_PROVIDERS
        or settings.calendar_connector.strip().lower() in OUTLOOK_PROVIDERS
    )


def google_connectors_enabled(settings: Settings) -> bool:
    return (
        settings.inbox_connector.strip().lower() in GOOGLE_INBOX_PROVIDERS
        or settings.calendar_connector.strip().lower() in GOOGLE_CALENDAR_PROVIDERS
    )


def rewrite_env_values(path: Path, values: dict[str, str]) -> None:
    if not path.exists():
        raise ProviderAuthError(f"Cannot write token because {path} does not exist.")
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


def load_secret_file(path_value: Optional[str]) -> dict[str, str]:
    if not path_value:
        return {}
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProviderAuthError(f"Failed to load provider secret file {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ProviderAuthError(f"Provider secret file {path} must contain a JSON object.")
    return {str(key).upper(): str(value) for key, value in payload.items() if value is not None}


def write_secret_file(path_value: Optional[str], values: dict[str, str]) -> None:
    if not path_value or not values:
        return
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    current: dict[str, Any] = {}
    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                current = loaded
        except (OSError, json.JSONDecodeError) as exc:
            raise ProviderAuthError(f"Failed to update provider secret file {path}: {exc}") from exc
    current.update(values)
    path.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def hydrate_provider_settings(settings: Settings) -> Settings:
    google_secret_values = load_secret_file(settings.google_secrets_path)
    graph_secret_values = load_secret_file(settings.microsoft_graph_secrets_path)
    updates: dict[str, Any] = {}

    secret_to_field = {
        "GOOGLE_CLIENT_ID": "google_client_id",
        "GOOGLE_CLIENT_SECRET": "google_client_secret",
        "GOOGLE_ACCESS_TOKEN": "google_access_token",
        "GOOGLE_REFRESH_TOKEN": "google_refresh_token",
        "OUTLOOK_TENANT_ID": "outlook_tenant_id",
        "OUTLOOK_CLIENT_ID": "outlook_client_id",
        "OUTLOOK_CLIENT_SECRET": "outlook_client_secret",
        "MICROSOFT_GRAPH_ACCESS_TOKEN": "microsoft_graph_access_token",
        "MICROSOFT_GRAPH_REFRESH_TOKEN": "microsoft_graph_refresh_token",
    }
    merged = {**google_secret_values, **graph_secret_values}
    for env_key, field_name in secret_to_field.items():
        if getattr(settings, field_name) in (None, "") and env_key in merged:
            updates[field_name] = merged[env_key]
    return settings.model_copy(update=updates) if updates else settings


def persist_provider_tokens(provider_id: str, token_payload: dict[str, Any], *, settings: Settings, env_path: Path = ENV_PATH) -> None:
    values: dict[str, str] = {}
    if provider_id == "google":
        if token_payload.get("access_token"):
            values["GOOGLE_ACCESS_TOKEN"] = str(token_payload["access_token"])
            os.environ["GOOGLE_ACCESS_TOKEN"] = values["GOOGLE_ACCESS_TOKEN"]
        if token_payload.get("refresh_token"):
            values["GOOGLE_REFRESH_TOKEN"] = str(token_payload["refresh_token"])
            os.environ["GOOGLE_REFRESH_TOKEN"] = values["GOOGLE_REFRESH_TOKEN"]
        write_secret_file(settings.google_secrets_path, values)
    elif provider_id == "microsoft_graph":
        if token_payload.get("access_token"):
            values["MICROSOFT_GRAPH_ACCESS_TOKEN"] = str(token_payload["access_token"])
            os.environ["MICROSOFT_GRAPH_ACCESS_TOKEN"] = values["MICROSOFT_GRAPH_ACCESS_TOKEN"]
        if token_payload.get("refresh_token"):
            values["MICROSOFT_GRAPH_REFRESH_TOKEN"] = str(token_payload["refresh_token"])
            os.environ["MICROSOFT_GRAPH_REFRESH_TOKEN"] = values["MICROSOFT_GRAPH_REFRESH_TOKEN"]
        write_secret_file(settings.microsoft_graph_secrets_path, values)
    else:
        raise ProviderAuthError(f"Unsupported provider_id: {provider_id}")

    if values and env_path.exists():
        rewrite_env_values(env_path, values)


def refresh_google_access_token(settings: Settings, *, env_path: Path = ENV_PATH) -> dict[str, Any]:
    resolved = hydrate_provider_settings(settings)
    if not resolved.google_client_id or not resolved.google_client_secret:
        raise ProviderAuthError("Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET.")
    if not resolved.google_refresh_token:
        raise ProviderAuthError("Missing GOOGLE_REFRESH_TOKEN.")

    token_payload = post_form(
        resolved.google_token_uri,
        {
            "grant_type": "refresh_token",
            "client_id": resolved.google_client_id,
            "client_secret": resolved.google_client_secret,
            "refresh_token": resolved.google_refresh_token,
        },
    )
    if "access_token" not in token_payload:
        raise ProviderAuthError("Google refresh-token response did not include an access token.")
    persist_provider_tokens("google", token_payload, settings=resolved, env_path=env_path)
    return token_payload


def refresh_microsoft_graph_access_token(settings: Settings, *, env_path: Path = ENV_PATH) -> dict[str, Any]:
    resolved = hydrate_provider_settings(settings)
    if not resolved.outlook_tenant_id or not resolved.outlook_client_id:
        raise ProviderAuthError("Missing OUTLOOK_TENANT_ID or OUTLOOK_CLIENT_ID.")
    if not resolved.microsoft_graph_refresh_token:
        raise ProviderAuthError("Missing MICROSOFT_GRAPH_REFRESH_TOKEN.")

    form_data = {
        "grant_type": "refresh_token",
        "client_id": resolved.outlook_client_id,
        "refresh_token": resolved.microsoft_graph_refresh_token,
        "scope": resolved.outlook_graph_scopes,
    }
    if resolved.outlook_client_secret:
        form_data["client_secret"] = resolved.outlook_client_secret

    token_url = f"https://login.microsoftonline.com/{resolved.outlook_tenant_id}/oauth2/v2.0/token"
    token_payload = post_form(token_url, form_data)
    if "access_token" not in token_payload:
        raise ProviderAuthError("Refresh-token response did not include an access token.")
    persist_provider_tokens("microsoft_graph", token_payload, settings=resolved, env_path=env_path)
    return token_payload


def ensure_provider_tokens(
    settings: Settings,
    *,
    env_path: Path = ENV_PATH,
    force_refresh: bool = False,
) -> Settings:
    resolved = hydrate_provider_settings(settings)
    updates: dict[str, Any] = {}

    if google_connectors_enabled(resolved) and resolved.google_refresh_token and (
        force_refresh or not resolved.google_access_token
    ):
        token_payload = refresh_google_access_token(resolved, env_path=env_path)
        updates["google_access_token"] = token_payload.get("access_token", resolved.google_access_token)
        updates["google_refresh_token"] = token_payload.get("refresh_token", resolved.google_refresh_token)

    if outlook_connectors_enabled(resolved) and resolved.microsoft_graph_refresh_token and (
        force_refresh or not resolved.microsoft_graph_access_token
    ):
        token_payload = refresh_microsoft_graph_access_token(resolved, env_path=env_path)
        updates["microsoft_graph_access_token"] = token_payload.get(
            "access_token", resolved.microsoft_graph_access_token
        )
        updates["microsoft_graph_refresh_token"] = token_payload.get(
            "refresh_token", resolved.microsoft_graph_refresh_token
        )

    return resolved.model_copy(update=updates) if updates else resolved


def describe_provider_bootstrap(settings: Settings) -> ConnectorBootstrapStatusResponse:
    resolved = hydrate_provider_settings(settings)

    google_inbox_selected = resolved.inbox_connector.strip().lower() in GOOGLE_INBOX_PROVIDERS
    google_calendar_selected = resolved.calendar_connector.strip().lower() in GOOGLE_CALENDAR_PROVIDERS
    google_selected = google_inbox_selected or google_calendar_selected
    google_ready = bool(resolved.google_access_token or resolved.google_refresh_token)
    google_refresh_supported = bool(
        resolved.google_client_id and resolved.google_client_secret and resolved.google_refresh_token
    )

    graph_inbox_selected = resolved.inbox_connector.strip().lower() in OUTLOOK_PROVIDERS
    graph_calendar_selected = resolved.calendar_connector.strip().lower() in OUTLOOK_PROVIDERS
    graph_selected = graph_inbox_selected or graph_calendar_selected
    graph_ready = bool(resolved.microsoft_graph_access_token or resolved.microsoft_graph_refresh_token)
    graph_refresh_supported = bool(
        resolved.outlook_tenant_id and resolved.outlook_client_id and resolved.microsoft_graph_refresh_token
    )

    providers = [
        ProviderBootstrapStatus(
            provider_id="google",
            inbox_selected=google_inbox_selected,
            calendar_selected=google_calendar_selected,
            access_token_present=bool(resolved.google_access_token),
            refresh_token_present=bool(resolved.google_refresh_token),
            client_id_present=bool(resolved.google_client_id),
            client_secret_present=bool(resolved.google_client_secret),
            secret_store_path=resolved.google_secrets_path,
            refresh_supported=google_refresh_supported,
            status=(
                "ready"
                if google_selected and google_ready
                else "configured"
                if google_ready
                else "degraded"
                if google_selected
                else "disabled"
            ),
            detail=(
                "Google connectors are selected and token refresh is available."
                if google_selected and google_refresh_supported
                else "Google connectors are selected but need bootstrap credentials."
                if google_selected
                else "Google connector support is available but not selected."
            ),
        ),
        ProviderBootstrapStatus(
            provider_id="microsoft_graph",
            inbox_selected=graph_inbox_selected,
            calendar_selected=graph_calendar_selected,
            access_token_present=bool(resolved.microsoft_graph_access_token),
            refresh_token_present=bool(resolved.microsoft_graph_refresh_token),
            client_id_present=bool(resolved.outlook_client_id),
            client_secret_present=bool(resolved.outlook_client_secret),
            secret_store_path=resolved.microsoft_graph_secrets_path,
            refresh_supported=graph_refresh_supported,
            status=(
                "ready"
                if graph_selected and graph_ready
                else "configured"
                if graph_ready
                else "degraded"
                if graph_selected
                else "disabled"
            ),
            detail=(
                "Microsoft Graph connectors are selected and token refresh is available."
                if graph_selected and graph_refresh_supported
                else "Microsoft Graph connectors are selected but need bootstrap credentials."
                if graph_selected
                else "Microsoft Graph connector support is available but not selected."
            ),
        ),
    ]
    return ConnectorBootstrapStatusResponse(providers=providers)
