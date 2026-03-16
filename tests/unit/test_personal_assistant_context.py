# Copyright (c) Dario Pizzolante
import unittest
from datetime import datetime, timedelta, timezone

from app.models.connectors import CalendarEvent, ConnectorHealth, InboxMessage
from app.services.personal_assistant_context import PersonalAssistantContextService


class RecordingInboxConnector:
    connector_id = "recording-inbox"

    def __init__(self) -> None:
        self.since = None

    def healthcheck(self, account_id: str) -> ConnectorHealth:
        return ConnectorHealth(connector_id=self.connector_id, status="ok")

    def list_messages(self, *, account_id: str, since=None, folder: str = "inbox", limit: int = 50):
        self.since = since
        return [
            InboxMessage(
                message_id="m1",
                account_id=account_id,
                sender="client@example.com",
                recipients=["ceo@example.com"],
                subject="Ping",
                body_text="hello",
                received_at=datetime(2026, 3, 10, 8, 0, tzinfo=timezone.utc),
            )
        ]


class RecordingCalendarConnector:
    connector_id = "recording-calendar"

    def healthcheck(self, calendar_id: str) -> ConnectorHealth:
        return ConnectorHealth(connector_id=self.connector_id, status="ok")

    def list_events(self, *, calendar_id: str, start_at: datetime, end_at: datetime):
        return [
            CalendarEvent(
                event_id="e1",
                calendar_id=calendar_id,
                title="Client call",
                start_at=start_at + timedelta(hours=1),
                end_at=start_at + timedelta(hours=2),
            )
        ]


class FailingInboxConnector:
    connector_id = "failing-inbox"

    def healthcheck(self, account_id: str) -> ConnectorHealth:
        return ConnectorHealth(connector_id=self.connector_id, status="ok")

    def list_messages(self, *, account_id: str, since=None, folder: str = "inbox", limit: int = 50):
        raise RuntimeError("token expired")


class PersonalAssistantContextTests(unittest.TestCase):
    def test_build_context_uses_inbox_lookback_window(self) -> None:
        inbox = RecordingInboxConnector()
        calendar = RecordingCalendarConnector()
        service = PersonalAssistantContextService(inbox_connector=inbox, calendar_connector=calendar)
        start = datetime(2026, 3, 11, 9, 0, tzinfo=timezone.utc)

        context = service.build_context(
            account_id="me",
            calendar_id="primary",
            window_start=start,
            window_hours=12,
            inbox_lookback_hours=24,
        )

        self.assertEqual(inbox.since, start - timedelta(hours=24))
        self.assertEqual(len(context.inbox_messages), 1)
        self.assertEqual(len(context.calendar_events), 1)
        self.assertIsNotNone(context.inbox_health)
        self.assertEqual(context.inbox_health.status, "ok")

    def test_build_context_degrades_health_on_fetch_failure(self) -> None:
        service = PersonalAssistantContextService(
            inbox_connector=FailingInboxConnector(),
            calendar_connector=RecordingCalendarConnector(),
        )

        context = service.build_context(account_id="me", calendar_id="primary")

        self.assertEqual(context.inbox_messages, [])
        self.assertIsNotNone(context.inbox_health)
        self.assertEqual(context.inbox_health.status, "error")
        self.assertIn("token expired", context.inbox_health.detail or "")


if __name__ == "__main__":
    unittest.main()
