import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACK_ROOT = ROOT / "config" / "client-template"


class ClientTemplatePackTests(unittest.TestCase):
    def test_pack_contains_expected_artifacts(self) -> None:
        expected_files = [
            "README.md",
            "client.yaml",
            "deployment.env.example",
            "docker-compose.client.yaml",
            "storage-map.yaml",
        ]

        for relative_path in expected_files:
            artifact = PACK_ROOT / relative_path
            self.assertTrue(artifact.is_file(), f"Missing client template artifact: {relative_path}")

    def test_client_config_preserves_isolated_deployment_flag(self) -> None:
        client_config = (PACK_ROOT / "client.yaml").read_text(encoding="utf-8")

        self.assertIn("id: client-template", client_config)
        self.assertIn("isolated_deployment: true", client_config)

    def test_deployment_template_uses_client_scoped_identity(self) -> None:
        env_template = (PACK_ROOT / "deployment.env.example").read_text(encoding="utf-8")
        compose_template = (PACK_ROOT / "docker-compose.client.yaml").read_text(encoding="utf-8")
        storage_map = (PACK_ROOT / "storage-map.yaml").read_text(encoding="utf-8")

        self.assertIn("CLIENT_SLUG=client-template", env_template)
        self.assertIn("TENANT_ID=client-template", env_template)
        self.assertIn("container_name: ${CLIENT_SLUG:-client-template}-agent-platform-postgres", compose_template)
        self.assertIn("name: ${CLIENT_SLUG:-client-template}_postgres_data", compose_template)
        self.assertIn("documents_root: data/clients/client-template/documents", storage_map)
        self.assertIn("google_oauth: secrets/client-template/google-oauth.json", storage_map)


if __name__ == "__main__":
    unittest.main()
