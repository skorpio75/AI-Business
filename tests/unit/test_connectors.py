# Copyright (c) Dario Pizzolante
import unittest
from datetime import date, datetime, timezone

from app.connectors.factory import build_calendar_connector, build_inbox_connector
from app.connectors.gmail import GmailInboxConnector
from app.connectors.google_calendar import GoogleCalendarConnector
from app.connectors.microsoft_graph import MicrosoftGraphCalendarConnector, MicrosoftGraphInboxConnector
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

if __name__ == "__main__":
    unittest.main()
