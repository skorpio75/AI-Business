from pathlib import Path

from app.db.models import WorkflowRunORM
from tests.unit.base import ROOT, UnitTestCase


class UnitTestBaseTests(UnitTestCase):
    def test_root_points_to_repo_root(self) -> None:
        self.assertEqual(ROOT, self.ROOT)
        self.assertTrue((self.ROOT / "README.md").is_file())

    def test_build_settings_uses_local_overrides_without_env_file(self) -> None:
        settings = self.build_settings(app_name="test-app", env="test")

        self.assertEqual(settings.app_name, "test-app")
        self.assertEqual(settings.env, "test")

    def test_temporary_directory_returns_path_object(self) -> None:
        with self.temporary_directory() as directory:
            self.assertIsInstance(directory, Path)
            self.assertTrue(directory.is_dir())

        self.assertFalse(directory.exists())

    def test_sqlite_session_bootstraps_metadata(self) -> None:
        with self.sqlite_session() as db:
            row = db.get(WorkflowRunORM, "missing")

        self.assertIsNone(row)


if __name__ == "__main__":
    import unittest

    unittest.main()
