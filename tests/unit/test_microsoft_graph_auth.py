import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.core.settings import Settings
from app.services.microsoft_graph_auth import outlook_connectors_enabled, persist_tokens, refresh_access_token


class MicrosoftGraphAuthTests(unittest.TestCase):
    def test_outlook_connectors_enabled_when_outlook_selected(self) -> None:
        settings = Settings(_env_file=None, inbox_connector="outlook", calendar_connector="null")

        self.assertTrue(outlook_connectors_enabled(settings))

    def test_persist_tokens_writes_access_and_refresh_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text("MICROSOFT_GRAPH_ACCESS_TOKEN=\nMICROSOFT_GRAPH_REFRESH_TOKEN=\n", encoding="utf-8")

            persist_tokens(
                {"access_token": "access-123", "refresh_token": "refresh-456"},
                env_path=env_path,
            )

            contents = env_path.read_text(encoding="utf-8")
            self.assertIn("MICROSOFT_GRAPH_ACCESS_TOKEN=access-123", contents)
            self.assertIn("MICROSOFT_GRAPH_REFRESH_TOKEN=refresh-456", contents)

    def test_refresh_access_token_persists_rotated_tokens(self) -> None:
        settings = Settings(
            _env_file=None,
            outlook_tenant_id="tenant-id",
            outlook_client_id="client-id",
            outlook_graph_scopes="offline_access https://graph.microsoft.com/Mail.Read",
            microsoft_graph_refresh_token="refresh-123",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text("MICROSOFT_GRAPH_ACCESS_TOKEN=\nMICROSOFT_GRAPH_REFRESH_TOKEN=refresh-123\n", encoding="utf-8")

            with patch(
                "app.services.microsoft_graph_auth.post_form",
                return_value={"access_token": "new-access", "refresh_token": "new-refresh"},
            ) as mocked_post:
                token_payload = refresh_access_token(settings, env_path=env_path)

            self.assertEqual(token_payload["access_token"], "new-access")
            self.assertEqual(os.environ["MICROSOFT_GRAPH_ACCESS_TOKEN"], "new-access")
            self.assertEqual(os.environ["MICROSOFT_GRAPH_REFRESH_TOKEN"], "new-refresh")
            self.assertEqual(mocked_post.call_count, 1)
            contents = env_path.read_text(encoding="utf-8")
            self.assertIn("MICROSOFT_GRAPH_ACCESS_TOKEN=new-access", contents)
            self.assertIn("MICROSOFT_GRAPH_REFRESH_TOKEN=new-refresh", contents)


if __name__ == "__main__":
    unittest.main()
