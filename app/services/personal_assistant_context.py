# Copyright (c) Dario Pizzolante
from datetime import datetime, timedelta, timezone

from app.connectors.calendar import CalendarConnector, NullCalendarConnector
from app.connectors.inbox import InboxConnector, NullInboxConnector
from app.models.connectors import PersonalAssistantContext


class PersonalAssistantContextService:
    def __init__(
        self,
        inbox_connector: InboxConnector | None = None,
        calendar_connector: CalendarConnector | None = None,
    ) -> None:
        self.inbox_connector = inbox_connector or NullInboxConnector()
        self.calendar_connector = calendar_connector or NullCalendarConnector()

    def build_context(
        self,
        *,
        account_id: str,
        calendar_id: str,
        window_start: datetime | None = None,
        window_hours: int = 24,
        inbox_lookback_hours: int | None = None,
        inbox_limit: int = 25,
    ) -> PersonalAssistantContext:
        start = window_start or datetime.now(timezone.utc)
        end = start + timedelta(hours=window_hours)
        inbox_since = start - timedelta(hours=inbox_lookback_hours or window_hours)
        inbox_health = self.inbox_connector.healthcheck(account_id)
        calendar_health = self.calendar_connector.healthcheck(calendar_id)

        inbox_messages = []
        if inbox_health.status == "ok":
            try:
                inbox_messages = self.inbox_connector.list_messages(
                    account_id=account_id,
                    since=inbox_since,
                    limit=inbox_limit,
                )
            except Exception as exc:
                inbox_health = inbox_health.model_copy(update={"status": "error", "detail": str(exc)})

        calendar_events = []
        if calendar_health.status == "ok":
            try:
                calendar_events = self.calendar_connector.list_events(
                    calendar_id=calendar_id,
                    start_at=start,
                    end_at=end,
                )
            except Exception as exc:
                calendar_health = calendar_health.model_copy(update={"status": "error", "detail": str(exc)})

        return PersonalAssistantContext(
            account_id=account_id,
            calendar_id=calendar_id,
            window_start=start,
            window_end=end,
            inbox_messages=inbox_messages,
            calendar_events=calendar_events,
            inbox_health=inbox_health,
            calendar_health=calendar_health,
        )
