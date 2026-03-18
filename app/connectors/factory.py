# Copyright (c) Dario Pizzolante
from app.connectors.calendar import CalendarConnector, NullCalendarConnector
from app.connectors.gmail import GmailInboxConnector
from app.connectors.google_calendar import GoogleCalendarConnector
from app.connectors.inbox import InboxConnector, NullInboxConnector
from app.connectors.microsoft_graph import MicrosoftGraphCalendarConnector, MicrosoftGraphInboxConnector
from app.connectors.tasks import NullTaskConnector, TaskConnector
from app.connectors.zimbra import ZimbraCalendarConnector, ZimbraInboxConnector, ZimbraTaskConnector
from app.core.settings import Settings


def build_inbox_connector(settings: Settings) -> InboxConnector:
    provider = settings.inbox_connector.strip().lower()
    if provider == "gmail":
        return GmailInboxConnector(access_token=settings.google_access_token)
    if provider in {"microsoft_graph", "graph", "outlook"}:
        return MicrosoftGraphInboxConnector(access_token=settings.microsoft_graph_access_token)
    if provider == "zimbra":
        return ZimbraInboxConnector(
            base_url=settings.zimbra_base_url,
            access_token=settings.zimbra_access_token,
            username=settings.zimbra_username,
            password=settings.zimbra_password,
            principal_id=settings.personal_assistant_account_id,
            request_timeout=settings.zimbra_request_timeout_seconds,
        )
    return NullInboxConnector()


def build_calendar_connector(settings: Settings) -> CalendarConnector:
    provider = settings.calendar_connector.strip().lower()
    if provider in {"google", "google_calendar", "google-calendar"}:
        return GoogleCalendarConnector(access_token=settings.google_access_token)
    if provider in {"microsoft_graph", "graph", "outlook"}:
        return MicrosoftGraphCalendarConnector(
            access_token=settings.microsoft_graph_access_token,
            principal_id=settings.personal_assistant_account_id,
        )
    if provider == "zimbra":
        return ZimbraCalendarConnector(
            base_url=settings.zimbra_base_url,
            access_token=settings.zimbra_access_token,
            username=settings.zimbra_username,
            password=settings.zimbra_password,
            principal_id=settings.personal_assistant_account_id,
            request_timeout=settings.zimbra_request_timeout_seconds,
        )
    return NullCalendarConnector()


def build_task_connector(settings: Settings) -> TaskConnector:
    provider = settings.tasks_connector.strip().lower()
    if provider == "zimbra":
        return ZimbraTaskConnector(
            base_url=settings.zimbra_base_url,
            access_token=settings.zimbra_access_token,
            username=settings.zimbra_username,
            password=settings.zimbra_password,
            principal_id=settings.personal_assistant_account_id,
            request_timeout=settings.zimbra_request_timeout_seconds,
        )
    return NullTaskConnector()
