from pathlib import Path
from typing import Any

from app.core.settings import Settings
from app.services.provider_auth import (
    ENV_PATH,
    ProviderAuthError,
    outlook_connectors_enabled,
    post_form,
    persist_provider_tokens,
    refresh_microsoft_graph_access_token,
)


class MicrosoftGraphAuthError(ProviderAuthError):
    pass


def persist_tokens(token_payload: dict[str, Any], *, env_path: Path = ENV_PATH) -> None:
    settings = Settings()
    persist_provider_tokens("microsoft_graph", token_payload, settings=settings, env_path=env_path)


def refresh_access_token(settings: Settings, *, env_path: Path = ENV_PATH) -> dict[str, Any]:
    return refresh_microsoft_graph_access_token(settings, env_path=env_path)
