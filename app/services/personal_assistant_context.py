# Copyright (c) Dario Pizzolante
from datetime import datetime, timedelta, timezone

from app.connectors.calendar import CalendarConnector, NullCalendarConnector
from app.connectors.inbox import InboxConnector, NullInboxConnector
from app.connectors.tasks import NullTaskConnector, TaskConnector
from app.models.connectors import PersonalAssistantContext


class PersonalAssistantContextService:
    def __init__(
        self,
        inbox_connector: InboxConnector | None = None,
        calendar_connector: CalendarConnector | None = None,
        task_connector: TaskConnector | None = None,
    ) -> None:
        self.inbox_connector = inbox_connector or NullInboxConnector()
        self.calendar_connector = calendar_connector or NullCalendarConnector()
        self.task_connector = task_connector or NullTaskConnector()

    def build_context(
        self,
        *,
        account_id: str,
        calendar_id: str,
        task_list_id: str,
        window_start: datetime | None = None,
        window_hours: int = 24,
        inbox_lookback_hours: int | None = None,
        inbox_limit: int = 25,
        task_limit: int = 25,
        include_completed_tasks: bool = False,
    ) -> PersonalAssistantContext:
        start = window_start or datetime.now(timezone.utc)
        end = start + timedelta(hours=window_hours)
        inbox_since = start - timedelta(hours=inbox_lookback_hours or window_hours)
        inbox_health = self.inbox_connector.healthcheck(account_id)
        calendar_health = self.calendar_connector.healthcheck(calendar_id)
        tasks_health = self.task_connector.healthcheck(task_list_id)

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

        todo_tasks = []
        if tasks_health.status == "ok":
            try:
                todo_tasks = self.task_connector.list_tasks(
                    list_id=task_list_id,
                    since=inbox_since,
                    limit=task_limit,
                    include_completed=include_completed_tasks,
                )
            except Exception as exc:
                tasks_health = tasks_health.model_copy(update={"status": "error", "detail": str(exc)})

        return PersonalAssistantContext(
            account_id=account_id,
            calendar_id=calendar_id,
            task_list_id=task_list_id,
            window_start=start,
            window_end=end,
            inbox_messages=inbox_messages,
            calendar_events=calendar_events,
            todo_tasks=todo_tasks,
            inbox_health=inbox_health,
            calendar_health=calendar_health,
            tasks_health=tasks_health,
        )
