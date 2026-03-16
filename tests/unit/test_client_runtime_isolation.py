# Copyright (c) Dario Pizzolante
import unittest
from pathlib import Path
import shutil
import uuid

from pydantic import ValidationError

from app.core.settings import ROOT, Settings, ensure_runtime_directories
from tests.sample_data import track_b_runtime_paths, track_b_settings_kwargs


class ClientRuntimeIsolationTests(unittest.TestCase):
    def test_track_b_settings_accept_tenant_scoped_paths(self) -> None:
        settings = Settings(_env_file=None, **track_b_settings_kwargs(ROOT, "acme"))

        self.assertEqual(settings.resolved_env_file, ROOT / "config" / "clients" / "acme.env")
        self.assertEqual(settings.resolved_client_documents_dir, ROOT / "data" / "clients" / "acme" / "documents")
        self.assertEqual(
            settings.resolved_client_prompt_override_dir,
            ROOT / "prompts" / "clients" / "acme",
        )

    def test_track_b_settings_reject_shared_secret_path(self) -> None:
        with self.assertRaises(ValidationError):
            Settings(
                _env_file=None,
                **track_b_settings_kwargs(
                    ROOT,
                    "acme",
                    google_secrets_path="secrets/internal/google-oauth.json",
                ),
            )

    def test_ensure_runtime_directories_creates_tenant_scoped_roots(self) -> None:
        tenant = f"acme-test-{uuid.uuid4().hex[:8]}"
        paths = track_b_runtime_paths(ROOT, tenant)
        env_path = paths["env_path"]
        data_root = paths["data_root"]
        prompt_root = paths["prompt_root"]
        secret_root = paths["secret_root"]
        try:
            env_path.parent.mkdir(parents=True, exist_ok=True)
            env_path.write_text("", encoding="utf-8")
            settings = Settings(_env_file=None, **track_b_settings_kwargs(ROOT, tenant))

            ensure_runtime_directories(settings)

            self.assertTrue(settings.resolved_client_documents_dir.is_dir())
            self.assertTrue(settings.resolved_client_logs_dir.is_dir())
            self.assertTrue(settings.resolved_client_exports_dir.is_dir())
            self.assertTrue(settings.resolved_client_vector_dir.is_dir())
            self.assertTrue(settings.resolved_client_prompt_override_dir.is_dir())
            self.assertTrue(secret_root.is_dir())
        finally:
            shutil.rmtree(data_root, ignore_errors=True)
            shutil.rmtree(prompt_root, ignore_errors=True)
            shutil.rmtree(secret_root, ignore_errors=True)
            if env_path.exists():
                env_path.unlink()


if __name__ == "__main__":
    unittest.main()
