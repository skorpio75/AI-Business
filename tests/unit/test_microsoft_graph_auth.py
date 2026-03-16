import os
import shutil
import unittest
from pathlib import Path
import uuid
from unittest.mock import patch

from app.core.settings import Settings
from app.services.microsoft_graph_auth import outlook_connectors_enabled, persist_tokens, refresh_access_token


class MicrosoftGraphAuthTests(unittest.TestCase):
    def test_outlook_connectors_enabled_when_outlook_selected(self) -> None:
        settings = Settings(_env_file=None, inbox_connector="outlook", calendar_connector="null")

        self.assertTrue(outlook_connectors_enabled(settings))

    def test_persist_tokens_writes_access_and_refresh_tokens(self) -> None:
        root = Path(__file__).resolve().parents[2]
        tenant = f"client-a-test-{uuid.uuid4().hex[:8]}"
        env_path = root / "config" / "clients" / f"{tenant}.env"
        secret_path = root / "secrets" / tenant / "microsoft-graph.json"
        data_root = root / "data" / "clients" / tenant
        prompt_root = root / "prompts" / "clients" / tenant
        try:
            env_path.parent.mkdir(parents=True, exist_ok=True)
            env_path.write_text("MICROSOFT_GRAPH_ACCESS_TOKEN=\nMICROSOFT_GRAPH_REFRESH_TOKEN=\n", encoding="utf-8")
            settings = Settings(
                _env_file=None,
                primary_track="track_b_client",
                tenant_id=tenant,
                runtime_env_file=str(env_path),
                client_documents_dir=str(data_root / "documents"),
                client_logs_dir=str(data_root / "logs"),
                client_exports_dir=str(data_root / "exports"),
                client_vector_dir=str(data_root / "vector"),
                client_prompt_override_dir=str(prompt_root),
                microsoft_graph_secrets_path=str(secret_path),
            )

            persist_tokens(
                {"access_token": "access-123", "refresh_token": "refresh-456"},
                settings=settings,
            )

            contents = env_path.read_text(encoding="utf-8")
            self.assertIn("MICROSOFT_GRAPH_ACCESS_TOKEN=access-123", contents)
            self.assertIn("MICROSOFT_GRAPH_REFRESH_TOKEN=refresh-456", contents)
            secret_contents = secret_path.read_text(encoding="utf-8")
            self.assertIn("access-123", secret_contents)
            self.assertIn("refresh-456", secret_contents)
        finally:
            shutil.rmtree(data_root, ignore_errors=True)
            shutil.rmtree(prompt_root, ignore_errors=True)
            shutil.rmtree(root / "secrets" / tenant, ignore_errors=True)
            if env_path.exists():
                env_path.unlink()

    def test_refresh_access_token_persists_rotated_tokens(self) -> None:
        root = Path(__file__).resolve().parents[2]
        tenant = f"client-a-test-{uuid.uuid4().hex[:8]}"
        env_path = root / "config" / "clients" / f"{tenant}.env"
        secret_path = root / "secrets" / tenant / "microsoft-graph.json"
        data_root = root / "data" / "clients" / tenant
        prompt_root = root / "prompts" / "clients" / tenant
        try:
            env_path.parent.mkdir(parents=True, exist_ok=True)
            env_path.write_text("MICROSOFT_GRAPH_ACCESS_TOKEN=\nMICROSOFT_GRAPH_REFRESH_TOKEN=refresh-123\n", encoding="utf-8")
            settings = Settings(
                _env_file=None,
                primary_track="track_b_client",
                tenant_id=tenant,
                runtime_env_file=str(env_path),
                outlook_tenant_id="tenant-id",
                outlook_client_id="client-id",
                outlook_graph_scopes="offline_access https://graph.microsoft.com/Mail.Read",
                microsoft_graph_refresh_token="refresh-123",
                client_documents_dir=str(data_root / "documents"),
                client_logs_dir=str(data_root / "logs"),
                client_exports_dir=str(data_root / "exports"),
                client_vector_dir=str(data_root / "vector"),
                client_prompt_override_dir=str(prompt_root),
                microsoft_graph_secrets_path=str(secret_path),
            )

            with patch(
                "app.services.provider_auth.post_form",
                return_value={"access_token": "new-access", "refresh_token": "new-refresh"},
            ) as mocked_post:
                token_payload = refresh_access_token(settings)

            self.assertEqual(token_payload["access_token"], "new-access")
            self.assertEqual(os.environ["MICROSOFT_GRAPH_ACCESS_TOKEN"], "new-access")
            self.assertEqual(os.environ["MICROSOFT_GRAPH_REFRESH_TOKEN"], "new-refresh")
            self.assertEqual(mocked_post.call_count, 1)
            contents = env_path.read_text(encoding="utf-8")
            self.assertIn("MICROSOFT_GRAPH_ACCESS_TOKEN=new-access", contents)
            self.assertIn("MICROSOFT_GRAPH_REFRESH_TOKEN=new-refresh", contents)
            secret_contents = secret_path.read_text(encoding="utf-8")
            self.assertIn("new-access", secret_contents)
            self.assertIn("new-refresh", secret_contents)
        finally:
            shutil.rmtree(data_root, ignore_errors=True)
            shutil.rmtree(prompt_root, ignore_errors=True)
            shutil.rmtree(root / "secrets" / tenant, ignore_errors=True)
            if env_path.exists():
                env_path.unlink()


if __name__ == "__main__":
    unittest.main()
