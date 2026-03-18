# Copyright (c) Dario Pizzolante
from datetime import datetime
from typing import Protocol

from app.models.connectors import ConnectorHealth, TaskSyncCursor, TodoTask


class TaskConnector(Protocol):
    connector_id: str

    def healthcheck(self, list_id: str) -> ConnectorHealth:
        """Return the current connector status for the target task list."""

    def list_tasks(
        self,
        *,
        list_id: str,
        since: datetime | None = None,
        limit: int = 50,
        include_completed: bool = False,
    ) -> list[TodoTask]:
        """Return normalized tasks for workflow consumption."""

    def pull_incremental(
        self,
        *,
        list_id: str,
        cursor: TaskSyncCursor | None = None,
        limit: int = 100,
        include_completed: bool = False,
    ) -> tuple[list[TodoTask], TaskSyncCursor]:
        """Return only new or changed tasks since the last sync."""


class NullTaskConnector:
    connector_id = "null-tasks"

    def healthcheck(self, list_id: str) -> ConnectorHealth:
        return ConnectorHealth(
            connector_id=self.connector_id,
            status="degraded",
            detail=f"No task connector configured for {list_id}.",
        )

    def list_tasks(
        self,
        *,
        list_id: str,
        since: datetime | None = None,
        limit: int = 50,
        include_completed: bool = False,
    ) -> list[TodoTask]:
        del since, limit, include_completed
        return []

    def pull_incremental(
        self,
        *,
        list_id: str,
        cursor: TaskSyncCursor | None = None,
        limit: int = 100,
        include_completed: bool = False,
    ) -> tuple[list[TodoTask], TaskSyncCursor]:
        del cursor, limit, include_completed
        return [], TaskSyncCursor(list_id=list_id)
