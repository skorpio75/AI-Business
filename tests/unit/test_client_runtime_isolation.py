import unittest
from pathlib import Path
import shutil
import uuid

from pydantic import ValidationError

from app.core.settings import ROOT, Settings, ensure_runtime_directories


class ClientRuntimeIsolationTests(unittest.TestCase):
    def test_track_b_settings_accept_tenant_scoped_paths(self) -> None:
        settings = Settings(
            _env_file=None,
            primary_track="track_b_client",
            tenant_id="acme",
            runtime_env_file="config/clients/acme.env",
            client_documents_dir="data/clients/acme/documents",
            client_logs_dir="data/clients/acme/logs",
            client_exports_dir="data/clients/acme/exports",
            client_vector_dir="data/clients/acme/vector",
            client_prompt_override_dir="prompts/clients/acme",
            google_secrets_path="secrets/acme/google-oauth.json",
            microsoft_graph_secrets_path="secrets/acme/microsoft-graph.json",
        )

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
                primary_track="track_b_client",
                tenant_id="acme",
                runtime_env_file="config/clients/acme.env",
                client_documents_dir="data/clients/acme/documents",
                client_logs_dir="data/clients/acme/logs",
                client_exports_dir="data/clients/acme/exports",
                client_vector_dir="data/clients/acme/vector",
                client_prompt_override_dir="prompts/clients/acme",
                google_secrets_path="secrets/internal/google-oauth.json",
            )

    def test_ensure_runtime_directories_creates_tenant_scoped_roots(self) -> None:
        tenant = f"acme-test-{uuid.uuid4().hex[:8]}"
        env_path = ROOT / "config" / "clients" / f"{tenant}.env"
        data_root = ROOT / "data" / "clients" / tenant
        prompt_root = ROOT / "prompts" / "clients" / tenant
        secret_root = ROOT / "secrets" / tenant
        try:
            env_path.parent.mkdir(parents=True, exist_ok=True)
            env_path.write_text("", encoding="utf-8")
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
                google_secrets_path=str(secret_root / "google-oauth.json"),
                microsoft_graph_secrets_path=str(secret_root / "microsoft-graph.json"),
            )

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
