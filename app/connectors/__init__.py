# Copyright (c) Dario Pizzolante
from app.connectors.calendar import CalendarConnector, NullCalendarConnector
from app.connectors.factory import build_calendar_connector, build_inbox_connector, build_task_connector
from app.connectors.gmail import GmailInboxConnector
from app.connectors.google_calendar import GoogleCalendarConnector
from app.connectors.inbox import InboxConnector, NullInboxConnector
from app.connectors.microsoft_graph import MicrosoftGraphCalendarConnector, MicrosoftGraphInboxConnector
from app.connectors.tasks import NullTaskConnector, TaskConnector
from app.connectors.zimbra import ZimbraCalendarConnector, ZimbraInboxConnector, ZimbraTaskConnector

__all__ = [
    "CalendarConnector",
    "InboxConnector",
    "TaskConnector",
    "GmailInboxConnector",
    "GoogleCalendarConnector",
    "MicrosoftGraphCalendarConnector",
    "MicrosoftGraphInboxConnector",
    "NullCalendarConnector",
    "NullInboxConnector",
    "NullTaskConnector",
    "ZimbraCalendarConnector",
    "ZimbraInboxConnector",
    "ZimbraTaskConnector",
    "build_calendar_connector",
    "build_inbox_connector",
    "build_task_connector",
]
