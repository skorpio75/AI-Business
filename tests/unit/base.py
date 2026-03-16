# Copyright (c) Dario Pizzolante
import os
import shutil
import tempfile
import unittest
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.settings import ROOT as APP_ROOT
from app.core.settings import Settings, ensure_runtime_directories, get_settings
from app.db.base import Base
from scripts.seed_config import SeedResult, seed_client_instance


ROOT = Path(__file__).resolve().parents[2]


class UnitTestCase(unittest.TestCase):
    ROOT = ROOT

    def build_settings(self, **overrides: object) -> Settings:
        return Settings(_env_file=None, **overrides)

    @contextmanager
    def temporary_directory(self) -> Iterator[Path]:
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @contextmanager
    def sqlite_session(self) -> Iterator[Session]:
        engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(engine)
        with Session(engine) as db:
            yield db


class TrackBSeededClientTestCase(UnitTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._seeded_results: list[SeedResult] = []
        self._original_runtime_env_file = os.environ.get("RUNTIME_ENV_FILE")
        get_settings.cache_clear()

    def tearDown(self) -> None:
        if self._original_runtime_env_file is None:
            os.environ.pop("RUNTIME_ENV_FILE", None)
        else:
            os.environ["RUNTIME_ENV_FILE"] = self._original_runtime_env_file
        get_settings.cache_clear()

        for result in reversed(self._seeded_results):
            self.cleanup_seeded_client(result)
        super().tearDown()

    def seed_track_b_client(
        self,
        name: str,
        *,
        api_port: int,
        postgres_port: int,
        tenant_prefix: str = "track-b-test",
    ) -> SeedResult:
        tenant_id = f"{tenant_prefix}-{uuid.uuid4().hex[:8]}"
        result = seed_client_instance(
            client_id=name,
            name=name,
            tenant_id=tenant_id,
            output_root=APP_ROOT,
            api_port=api_port,
            postgres_port=postgres_port,
        )
        self._seeded_results.append(result)
        return result

    def activate_seeded_client(self, result: SeedResult) -> Settings:
        os.environ["RUNTIME_ENV_FILE"] = str(result.runtime_env_path.relative_to(APP_ROOT))
        get_settings.cache_clear()
        settings = get_settings()
        ensure_runtime_directories(settings)
        return settings

    def cleanup_seeded_client(self, result: SeedResult) -> None:
        shutil.rmtree(APP_ROOT / "data" / "clients" / result.tenant_id, ignore_errors=True)
        shutil.rmtree(APP_ROOT / "prompts" / "clients" / result.tenant_id, ignore_errors=True)
        shutil.rmtree(APP_ROOT / "secrets" / result.tenant_id, ignore_errors=True)
        if result.client_config_path.exists():
            result.client_config_path.unlink()
        if result.runtime_env_path.exists():
            result.runtime_env_path.unlink()
