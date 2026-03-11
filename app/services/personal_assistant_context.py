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
        inbox_limit: int = 25,
    ) -> PersonalAssistantContext:
        start = window_start or datetime.now(timezone.utc)
        end = start + timedelta(hours=window_hours)
        return PersonalAssistantContext(
            account_id=account_id,
            calendar_id=calendar_id,
            window_start=start,
            window_end=end,
            inbox_messages=self.inbox_connector.list_messages(
                account_id=account_id,
                since=start,
                limit=inbox_limit,
            ),
            calendar_events=self.calendar_connector.list_events(
                calendar_id=calendar_id,
                start_at=start,
                end_at=end,
            ),
            inbox_health=self.inbox_connector.healthcheck(account_id),
            calendar_health=self.calendar_connector.healthcheck(calendar_id),
        )
