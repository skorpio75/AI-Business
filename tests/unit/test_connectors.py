# Copyright (c) Dario Pizzolante
import unittest
from datetime import date, datetime, timezone

from app.connectors.factory import build_calendar_connector, build_inbox_connector, build_task_connector
from app.connectors.gmail import GmailInboxConnector
from app.connectors.google_calendar import GoogleCalendarConnector
from app.connectors.microsoft_graph import MicrosoftGraphCalendarConnector, MicrosoftGraphInboxConnector
from app.connectors.zimbra import ZimbraCalendarConnector, ZimbraInboxConnector, ZimbraTaskConnector
from app.core.settings import Settings


class ConnectorFactoryTests(unittest.TestCase):
    def test_build_inbox_connector_gmail(self) -> None:
        settings = Settings(_env_file=None, inbox_connector="gmail", google_access_token="token")

        connector = build_inbox_connector(settings)

        self.assertIsInstance(connector, GmailInboxConnector)

    def test_build_calendar_connector_microsoft_graph_uses_principal(self) -> None:
        settings = Settings(
            _env_file=None,
            calendar_connector="microsoft_graph",
            microsoft_graph_access_token="token",
            personal_assistant_account_id="ceo@company.test",
        )

        connector = build_calendar_connector(settings)

        self.assertIsInstance(connector, MicrosoftGraphCalendarConnector)
        self.assertEqual(connector.principal_id, "ceo@company.test")

    def test_build_inbox_connector_microsoft_graph(self) -> None:
        settings = Settings(_env_file=None, inbox_connector="outlook", microsoft_graph_access_token="token")

        connector = build_inbox_connector(settings)

        self.assertIsInstance(connector, MicrosoftGraphInboxConnector)

    def test_build_connectors_zimbra(self) -> None:
        settings = Settings(
            _env_file=None,
            inbox_connector="zimbra",
            calendar_connector="zimbra",
            tasks_connector="zimbra",
            zimbra_base_url="https://mail.example.com",
            zimbra_username="ceo@example.com",
            zimbra_password="secret",
            personal_assistant_account_id="dario.pizzolante@stratevia.eu",
        )

        inbox_connector = build_inbox_connector(settings)
        calendar_connector = build_calendar_connector(settings)
        task_connector = build_task_connector(settings)

        self.assertIsInstance(inbox_connector, ZimbraInboxConnector)
        self.assertIsInstance(calendar_connector, ZimbraCalendarConnector)
        self.assertIsInstance(task_connector, ZimbraTaskConnector)
        self.assertEqual(calendar_connector.principal_id, "dario.pizzolante@stratevia.eu")
        self.assertEqual(task_connector.principal_id, "dario.pizzolante@stratevia.eu")


class ConnectorNormalizationTests(unittest.TestCase):
    def test_gmail_normalize_message_decodes_plain_text_body(self) -> None:
        connector = GmailInboxConnector(access_token="token")
        payload = {
            "id": "msg-1",
            "threadId": "thread-1",
            "internalDate": "1710151200000",
            "labelIds": ["INBOX", "UNREAD"],
            "payload": {
                "headers": [
                    {"name": "From", "value": "client@example.com"},
                    {"name": "To", "value": "ceo@example.com"},
                    {"name": "Subject", "value": "Need proposal"},
                ],
                "parts": [
                    {
                        "mimeType": "text/plain",
                        "body": {"data": "SGVsbG8gZnJvbSBHbWFpbA"},
                    }
                ],
            },
            "snippet": "Hello from Gmail",
        }

        message = connector._normalize_message(account_id="me", payload=payload)

        self.assertIsNotNone(message)
        self.assertEqual(message.body_text, "Hello from Gmail")
        self.assertEqual(message.subject, "Need proposal")
        self.assertTrue(message.is_unread)

    def test_google_calendar_normalize_event_handles_all_day_items(self) -> None:
        connector = GoogleCalendarConnector(access_token="token")
        payload = {
            "id": "evt-1",
            "summary": "Strategy offsite",
            "start": {"date": "2026-03-20"},
            "end": {"date": "2026-03-21"},
            "organizer": {"email": "ceo@example.com"},
            "attendees": [{"email": "ceo@example.com", "self": True, "responseStatus": "accepted"}],
            "status": "confirmed",
        }

        event = connector._normalize_event(calendar_id="primary", payload=payload)

        self.assertIsNotNone(event)
        self.assertTrue(event.is_all_day)
        self.assertEqual(
            event.start_at,
            datetime.combine(date(2026, 3, 20), datetime.min.time(), tzinfo=timezone.utc),
        )
        self.assertEqual(
            event.end_at,
            datetime.combine(date(2026, 3, 21), datetime.min.time(), tzinfo=timezone.utc),
        )

    def test_zimbra_inbox_list_messages_normalizes_rest_payload(self) -> None:
        connector = ZimbraInboxConnector(
            base_url="https://mail.example.com",
            username="dario.pizzolante@stratevia.eu",
            password="secret",
        )
        payload = {
            "_attrs": {"id": "1"},
            "m": [
                {
                    "id": "msg-1",
                    "cid": "conv-1",
                    "su": "Need proposal",
                    "fr": "client@example.com",
                    "e": [{"a": "dario.pizzolante@stratevia.eu"}],
                    "d": "1710151200000",
                    "f": "u",
                    "desc": "Please send the first draft.",
                }
            ],
        }
        connector._get_folder_payload = lambda **kwargs: payload  # type: ignore[method-assign]

        messages = connector.list_messages(account_id="dario.pizzolante@stratevia.eu")

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].subject, "Need proposal")
        self.assertEqual(messages[0].sender, "client@example.com")
        self.assertTrue(messages[0].is_unread)

    def test_zimbra_calendar_list_events_normalizes_payload(self) -> None:
        connector = ZimbraCalendarConnector(
            base_url="https://mail.example.com",
            username="dario.pizzolante@stratevia.eu",
            password="secret",
            principal_id="dario.pizzolante@stratevia.eu",
        )
        payload = {
            "appt": [
                {
                    "id": "evt-1",
                    "name": "Client workshop",
                    "s": "20260320T090000Z",
                    "e": "20260320T100000Z",
                    "loc": "Teams",
                    "desc": "Review the roadmap",
                    "at": [{"a": "client@example.com"}, {"a": "dario.pizzolante@stratevia.eu"}],
                }
            ]
        }
        connector._get_folder_payload = lambda **kwargs: payload  # type: ignore[method-assign]

        events = connector.list_events(
            calendar_id="primary",
            start_at=datetime(2026, 3, 20, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2026, 3, 21, 0, 0, tzinfo=timezone.utc),
        )

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].title, "Client workshop")
        self.assertEqual(events[0].location, "Teams")
        self.assertEqual(events[0].attendees, ["client@example.com", "dario.pizzolante@stratevia.eu"])

    def test_zimbra_task_list_normalizes_payload(self) -> None:
        connector = ZimbraTaskConnector(
            base_url="https://mail.example.com",
            username="dario.pizzolante@stratevia.eu",
            password="secret",
            principal_id="dario.pizzolante@stratevia.eu",
        )
        payload = {
            "task": [
                {
                    "id": "task-1",
                    "name": "Reply to client",
                    "due": "20260321T150000Z",
                    "priority": "1",
                    "desc": "Prepare the follow-up note.",
                }
            ]
        }
        connector._get_folder_payload = lambda **kwargs: payload  # type: ignore[method-assign]

        tasks = connector.list_tasks(list_id="Tasks")

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Reply to client")
        self.assertEqual(tasks[0].priority, "high")
        self.assertEqual(tasks[0].status, "not_started")

if __name__ == "__main__":
    unittest.main()
