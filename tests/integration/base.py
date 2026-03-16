from contextlib import ExitStack
from typing import Iterator
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.api import main as api_main
from tests.unit.base import UnitTestCase


class ApiIntegrationTestCase(UnitTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._patches = ExitStack()
        self.addCleanup(self._patches.close)

        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            future=True,
        )
        Base.metadata.create_all(engine)
        self._session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

        def override_get_db() -> Iterator[Session]:
            db = self._session_factory()
            try:
                yield db
            finally:
                db.close()

        api_main.app.dependency_overrides[api_main.get_db] = override_get_db
        self.addCleanup(api_main.app.dependency_overrides.clear)

        self._patches.enter_context(patch.object(api_main, "ensure_runtime_directories", lambda settings: None))
        self._patches.enter_context(patch.object(api_main, "bootstrap_provider_tokens_on_startup", lambda: None))
        self.client = self._patches.enter_context(TestClient(api_main.app))

    def patch_api_attr(self, name: str, value: object) -> None:
        self._patches.enter_context(patch.object(api_main, name, value))
