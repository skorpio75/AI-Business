import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK_PATH = ROOT / "docs" / "track-b-bootstrap-runbook.md"


class TrackBBootstrapRunbookTests(unittest.TestCase):
    def test_runbook_exists_and_covers_critical_bootstrap_steps(self) -> None:
        self.assertTrue(RUNBOOK_PATH.is_file(), "Missing Track B bootstrap runbook")
        text = RUNBOOK_PATH.read_text(encoding="utf-8")

        required_markers = [
            "RUNTIME_ENV_FILE",
            "scripts\\seed_config.py",
            "config/clients/<tenant>.env",
            "LANGFUSE_ENABLED",
            "docker compose -f docker-compose.yml -f config/client-template/docker-compose.client.yaml --env-file",
            "scripts\\init_db.py",
            "/healthz",
            "/connectors/bootstrap-status",
            "scripts\\google_oauth_local_server.py",
            "scripts\\microsoft_graph_device_code.py",
            "/knowledge/qna",
            "/workflows/email-operations/run",
        ]

        for marker in required_markers:
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
