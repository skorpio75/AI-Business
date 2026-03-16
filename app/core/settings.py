from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "enterprise-agent-platform"
    env: str = "local"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str = "postgresql+psycopg://agent:agent@localhost:5433/agent_platform"

    ollama_base_url: str = "http://localhost:11434"
    local_model: str = "qwen2.5:3b"
    model_timeout_seconds: float = 10.0
    cloud_model: str = "openai/gpt-4o-mini"
    openrouter_api_key: Optional[str] = None

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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
