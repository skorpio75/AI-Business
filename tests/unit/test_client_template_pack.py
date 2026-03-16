import unittest
from pathlib import Path

import yaml


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

    def test_client_config_defines_finalized_track_b_contract(self) -> None:
        client_config = yaml.safe_load((PACK_ROOT / "client.yaml").read_text(encoding="utf-8"))

        self.assertEqual(client_config["client"]["id"], "client-template")
        self.assertEqual(client_config["client"]["primary_track"], "track_b_client")
        self.assertTrue(client_config["client"]["isolated_deployment"])
        self.assertEqual(client_config["tenancy"]["tenant_id"], "client-template")
        self.assertEqual(client_config["tenancy"]["deployment_model"], "isolated_single_tenant")
        self.assertTrue(client_config["governance"]["approval_required_for_sensitive_actions"])
        self.assertEqual(
            client_config["deployment"]["compose"]["overlay_file"],
            "config/client-template/docker-compose.client.yaml",
        )
        self.assertEqual(client_config["storage"]["documents_root"], "data/clients/client-template/documents")
        self.assertEqual(client_config["models"]["routing_posture"], "governed_local_first")
        self.assertEqual(
            client_config["solution_pack"]["default_enabled_workflows"],
            ["knowledge-qna", "document-intake", "reporting"],
        )
        self.assertIn("email-operations", client_config["solution_pack"]["planned_workflow_portability"])
        self.assertEqual(
            client_config["runtime_defaults"]["operating_modes"],
            ["client_delivery", "client_facing_service"],
        )

    def test_deployment_template_uses_client_scoped_identity(self) -> None:
        env_template = (PACK_ROOT / "deployment.env.example").read_text(encoding="utf-8")
        compose_template = (PACK_ROOT / "docker-compose.client.yaml").read_text(encoding="utf-8")
        storage_map = (PACK_ROOT / "storage-map.yaml").read_text(encoding="utf-8")

        self.assertIn("CLIENT_SLUG=client-template", env_template)
        self.assertIn("TENANT_ID=client-template", env_template)
        self.assertIn("PRIMARY_TRACK=track_b_client", env_template)
        self.assertIn("RUNTIME_ENV_FILE=config/client-template/deployment.env.example", env_template)
        self.assertIn("LANGFUSE_ENABLED=false", env_template)
        self.assertIn("LANGFUSE_HOST=https://cloud.langfuse.com", env_template)
        self.assertIn("container_name: ${CLIENT_SLUG:-client-template}-agent-platform-postgres", compose_template)
        self.assertIn("name: ${CLIENT_SLUG:-client-template}_postgres_data", compose_template)
        self.assertIn("documents_root: data/clients/client-template/documents", storage_map)
        self.assertIn("google_oauth: secrets/client-template/google-oauth.json", storage_map)


if __name__ == "__main__":
    unittest.main()
