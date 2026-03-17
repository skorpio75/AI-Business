# Copyright (c) Dario Pizzolante
import os
from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENV_PATH = ROOT / ".env"


def _resolve_runtime_path(path_value: str | None) -> Path | None:
    if not path_value:
        return None
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    return path


def _is_within(path: Path, base: Path) -> bool:
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def resolve_env_file_path() -> Path:
    env_file = os.environ.get("RUNTIME_ENV_FILE")
    resolved = _resolve_runtime_path(env_file)
    return resolved or DEFAULT_ENV_PATH


class Settings(BaseSettings):
    app_name: str = "enterprise-agent-platform"
    env: str = "local"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str = "postgresql+psycopg://agent:agent@localhost:5433/agent_platform"
    primary_track: Literal["track_a_internal", "track_b_client"] = "track_a_internal"
    tenant_id: str = "internal"
    runtime_env_file: Optional[str] = None

    ollama_base_url: str = "http://localhost:11434"
    local_model: str = "qwen2.5:3b"
    model_timeout_seconds: float = 10.0
    cloud_model: str = "openai/gpt-4o-mini"
    openrouter_api_key: Optional[str] = None
    email_local_model: str = "llama3.2:3b"
    email_local_timeout_seconds: float = 30.0
    email_local_text_num_predict: int = 180
    email_strong_local_model: Optional[str] = "qwen2.5:1.5b-instruct-q4_K_M"
    email_strong_local_timeout_seconds: float = 60.0
    email_strong_local_text_num_predict: int = 220
    email_upgrade_on_weak_draft: bool = True
    email_cloud_max_tokens: int = 400
    langfuse_enabled: bool = False
    langfuse_public_key: Optional[str] = None
    langfuse_secret_key: Optional[str] = None
    langfuse_host: str = "https://cloud.langfuse.com"
    langfuse_release: Optional[str] = None

    local_confidence_threshold: float = 0.8
    max_local_input_chars: int = 3000
    force_local_only: bool = False
    knowledge_vector_dimensions: int = 8
    inbox_connector: str = "null"
    calendar_connector: str = "null"
    personal_assistant_account_id: str = "me"
    personal_assistant_calendar_id: str = "primary"
    personal_assistant_window_hours: int = 24
    personal_assistant_inbox_lookback_hours: int = 24
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_oauth_scopes: str = (
        "https://www.googleapis.com/auth/gmail.readonly "
        "https://www.googleapis.com/auth/calendar.readonly"
    )
    google_oauth_redirect_uri: str = "http://127.0.0.1:8765/oauth/google/callback"
    google_token_uri: str = "https://oauth2.googleapis.com/token"
    google_access_token: Optional[str] = None
    google_refresh_token: Optional[str] = None
    google_secrets_path: Optional[str] = None
    outlook_tenant_id: Optional[str] = None
    outlook_client_id: Optional[str] = None
    outlook_client_secret: Optional[str] = None
    outlook_graph_scopes: str = "offline_access https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/Calendars.Read"
    microsoft_graph_access_token: Optional[str] = None
    microsoft_graph_refresh_token: Optional[str] = None
    microsoft_graph_secrets_path: Optional[str] = None
    client_documents_dir: str = "data/internal/documents"
    client_logs_dir: str = "data/internal/logs"
    client_exports_dir: str = "data/internal/exports"
    client_vector_dir: str = "data/internal/vector"
    client_prompt_override_dir: str = "prompts/internal"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def resolved_env_file(self) -> Path:
        return _resolve_runtime_path(self.runtime_env_file) or DEFAULT_ENV_PATH

    @property
    def resolved_client_documents_dir(self) -> Path:
        return _resolve_runtime_path(self.client_documents_dir) or ROOT / "data" / "internal" / "documents"

    @property
    def resolved_client_logs_dir(self) -> Path:
        return _resolve_runtime_path(self.client_logs_dir) or ROOT / "data" / "internal" / "logs"

    @property
    def resolved_client_exports_dir(self) -> Path:
        return _resolve_runtime_path(self.client_exports_dir) or ROOT / "data" / "internal" / "exports"

    @property
    def resolved_client_vector_dir(self) -> Path:
        return _resolve_runtime_path(self.client_vector_dir) or ROOT / "data" / "internal" / "vector"

    @property
    def resolved_client_prompt_override_dir(self) -> Path:
        return _resolve_runtime_path(self.client_prompt_override_dir) or ROOT / "prompts" / "internal"

    @model_validator(mode="after")
    def validate_track_b_isolation(self) -> "Settings":
        if self.primary_track != "track_b_client":
            return self

        tenant = self.tenant_id.strip()
        if not tenant:
            raise ValueError("tenant_id is required when primary_track=track_b_client")
        if self.resolved_env_file == DEFAULT_ENV_PATH:
            raise ValueError("track_b_client requires RUNTIME_ENV_FILE so credentials do not fall back to the shared root .env")

        expected_storage_root = ROOT / "data" / "clients" / tenant
        expected_prompt_root = ROOT / "prompts" / "clients" / tenant
        expected_secret_root = ROOT / "secrets" / tenant

        storage_paths = {
            "client_documents_dir": self.resolved_client_documents_dir,
            "client_logs_dir": self.resolved_client_logs_dir,
            "client_exports_dir": self.resolved_client_exports_dir,
            "client_vector_dir": self.resolved_client_vector_dir,
        }
        for field_name, path in storage_paths.items():
            if not _is_within(path, expected_storage_root):
                raise ValueError(f"{field_name} must stay inside {expected_storage_root} for tenant {tenant}")

        if not _is_within(self.resolved_client_prompt_override_dir, expected_prompt_root):
            raise ValueError(
                f"client_prompt_override_dir must stay inside {expected_prompt_root} for tenant {tenant}"
            )

        for field_name, value in {
            "google_secrets_path": self.google_secrets_path,
            "microsoft_graph_secrets_path": self.microsoft_graph_secrets_path,
        }.items():
            if value:
                resolved = _resolve_runtime_path(value)
                if resolved is not None and not _is_within(resolved, expected_secret_root):
                    raise ValueError(f"{field_name} must stay inside {expected_secret_root} for tenant {tenant}")

        return self


def ensure_runtime_directories(settings: Settings) -> None:
    directories = [
        settings.resolved_client_documents_dir,
        settings.resolved_client_logs_dir,
        settings.resolved_client_exports_dir,
        settings.resolved_client_vector_dir,
        settings.resolved_client_prompt_override_dir,
    ]
    for path in directories:
        path.mkdir(parents=True, exist_ok=True)

    for secret_path in (settings.google_secrets_path, settings.microsoft_graph_secrets_path):
        resolved = _resolve_runtime_path(secret_path)
        if resolved is not None:
            resolved.parent.mkdir(parents=True, exist_ok=True)


def build_settings() -> Settings:
    return Settings(_env_file=resolve_env_file_path())


@lru_cache
def get_settings() -> Settings:
    return build_settings()
