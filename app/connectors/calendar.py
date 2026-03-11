from datetime import datetime
from typing import Protocol

from app.models.connectors import CalendarEvent, CalendarSyncCursor, ConnectorHealth


class CalendarConnector(Protocol):
    connector_id: str

    def healthcheck(self, calendar_id: str) -> ConnectorHealth:
        """Return the current connector status for the target calendar."""

    def list_events(
        self,
        *,
        calendar_id: str,
        start_at: datetime,
        end_at: datetime,
    ) -> list[CalendarEvent]:
        """Return normalized calendar events for workflow consumption."""

    def pull_incremental(
        self,
        *,
        calendar_id: str,
        cursor: CalendarSyncCursor | None = None,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
    ) -> tuple[list[CalendarEvent], CalendarSyncCursor]:
        """Return only new or changed calendar items since the last sync."""


class NullCalendarConnector:
    connector_id = "null-calendar"

    def healthcheck(self, calendar_id: str) -> ConnectorHealth:
        return ConnectorHealth(
            connector_id=self.connector_id,
            status="degraded",
            detail=f"No calendar connector configured for {calendar_id}.",
        )

    def list_events(
        self,
        *,
        calendar_id: str,
        start_at: datetime,
        end_at: datetime,
    ) -> list[CalendarEvent]:
        return []

    def pull_incremental(
        self,
        *,
        calendar_id: str,
        cursor: CalendarSyncCursor | None = None,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
    ) -> tuple[list[CalendarEvent], CalendarSyncCursor]:
        return [], CalendarSyncCursor(calendar_id=calendar_id)
