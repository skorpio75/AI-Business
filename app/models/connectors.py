from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field


InboxFolder = Literal["inbox", "sent", "archive"]
MessageDirection = Literal["inbound", "outbound"]
ConnectorStatus = Literal["ok", "degraded", "error"]
EventResponseStatus = Literal["accepted", "tentative", "declined", "needs_action"]


class ConnectorHealth(BaseModel):
    connector_id: str
    status: ConnectorStatus = "ok"
    checked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    detail: Optional[str] = None


class InboxMessage(BaseModel):
    message_id: str
    thread_id: Optional[str] = None
    account_id: str
    folder: InboxFolder = "inbox"
    direction: MessageDirection = "inbound"
    sender: str
    recipients: list[str] = Field(default_factory=list)
    subject: str
    body_text: str
    received_at: datetime
    is_unread: bool = True
    labels: list[str] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)


class InboxSyncCursor(BaseModel):
    account_id: str
    cursor: Optional[str] = None
    synced_at: Optional[datetime] = None


class CalendarEvent(BaseModel):
    event_id: str
    calendar_id: str
    title: str
    start_at: datetime
    end_at: datetime
    organizer: Optional[str] = None
    attendees: list[str] = Field(default_factory=list)
    location: Optional[str] = None
    description: Optional[str] = None
    response_status: EventResponseStatus = "accepted"
    is_all_day: bool = False
    metadata: dict[str, str] = Field(default_factory=dict)


class CalendarSyncCursor(BaseModel):
    calendar_id: str
    cursor: Optional[str] = None
    synced_at: Optional[datetime] = None


class PersonalAssistantContext(BaseModel):
    account_id: str
    calendar_id: str
    window_start: datetime
    window_end: datetime
    inbox_messages: list[InboxMessage] = Field(default_factory=list)
    calendar_events: list[CalendarEvent] = Field(default_factory=list)
    inbox_health: Optional[ConnectorHealth] = None
    calendar_health: Optional[ConnectorHealth] = None
