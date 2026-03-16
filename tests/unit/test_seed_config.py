import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.seed_config import seed_client_instance


class SeedConfigTests(unittest.TestCase):
    def test_seed_client_instance_materializes_client_contract_and_env(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir)

            result = seed_client_instance(
                client_id="Acme ERP Rollout",
                name="Acme ERP Rollout",
                tenant_id="acme-erp",
                postgres_port=5451,
                output_root=output_root,
            )

            self.assertTrue(result.client_config_path.is_file())
            self.assertTrue(result.runtime_env_path.is_file())
            for directory in result.created_directories:
                self.assertTrue(directory.is_dir())

            client_contract = yaml.safe_load(result.client_config_path.read_text(encoding="utf-8"))
            env_text = result.runtime_env_path.read_text(encoding="utf-8")

            self.assertEqual(client_contract["client"]["id"], "Acme ERP Rollout")
            self.assertEqual(client_contract["client"]["slug"], "acme-erp-rollout")
            self.assertEqual(client_contract["tenancy"]["tenant_id"], "acme-erp")
            self.assertEqual(client_contract["deployment"]["compose"]["env_file"], "config/clients/acme-erp.env")
            self.assertEqual(client_contract["storage"]["documents_root"], "data/clients/acme-erp/documents")
            self.assertIn("RUNTIME_ENV_FILE=config/clients/acme-erp.env", env_text)
            self.assertIn("POSTGRES_PORT=5451", env_text)
            self.assertIn("GOOGLE_SECRETS_PATH=secrets/acme-erp/google-oauth.json", env_text)

    def test_seed_client_instance_dry_run_does_not_write_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir)

            result = seed_client_instance(
                client_id="Beta Advisory",
                name="Beta Advisory",
                output_root=output_root,
                dry_run=True,
            )

            self.assertFalse(result.client_config_path.exists())
            self.assertFalse(result.runtime_env_path.exists())
            for directory in result.created_directories:
                self.assertFalse(directory.exists())

    def test_seed_client_instance_requires_force_to_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir)

            seed_client_instance(
                client_id="Gamma Delivery",
                name="Gamma Delivery",
                tenant_id="gamma-delivery",
                output_root=output_root,
            )

            with self.assertRaises(FileExistsError):
                seed_client_instance(
                    client_id="Gamma Delivery",
                    name="Gamma Delivery",
                    tenant_id="gamma-delivery",
                    output_root=output_root,
                )


if __name__ == "__main__":
    unittest.main()
