# Copyright (c) Dario Pizzolante
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field


InboxFolder = Literal["inbox", "sent", "archive"]
MessageDirection = Literal["inbound", "outbound"]
ConnectorStatus = Literal["ok", "degraded", "error"]
EventResponseStatus = Literal["accepted", "tentative", "declined", "needs_action"]
ProviderBootstrapState = Literal["disabled", "degraded", "configured", "ready"]
TaskStatus = Literal["not_started", "in_progress", "completed", "deferred", "waiting"]
TaskPriority = Literal["low", "normal", "high"]


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


class TodoTask(BaseModel):
    task_id: str
    list_id: str
    title: str
    body_text: Optional[str] = None
    due_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: TaskStatus = "not_started"
    priority: TaskPriority = "normal"
    web_link: Optional[str] = None
    metadata: dict[str, str] = Field(default_factory=dict)


class TaskSyncCursor(BaseModel):
    list_id: str
    cursor: Optional[str] = None
    synced_at: Optional[datetime] = None


class PersonalAssistantContext(BaseModel):
    account_id: str
    calendar_id: str
    task_list_id: str
    window_start: datetime
    window_end: datetime
    inbox_messages: list[InboxMessage] = Field(default_factory=list)
    calendar_events: list[CalendarEvent] = Field(default_factory=list)
    todo_tasks: list[TodoTask] = Field(default_factory=list)
    inbox_health: Optional[ConnectorHealth] = None
    calendar_health: Optional[ConnectorHealth] = None
    tasks_health: Optional[ConnectorHealth] = None


class ProviderBootstrapStatus(BaseModel):
    provider_id: str
    inbox_selected: bool = False
    calendar_selected: bool = False
    tasks_selected: bool = False
    access_token_present: bool = False
    refresh_token_present: bool = False
    client_id_present: bool = False
    client_secret_present: bool = False
    base_url_present: bool = False
    username_present: bool = False
    password_present: bool = False
    secret_store_path: Optional[str] = None
    refresh_supported: bool = False
    status: ProviderBootstrapState = "disabled"
    detail: str


class ConnectorBootstrapStatusResponse(BaseModel):
    providers: list[ProviderBootstrapStatus] = Field(default_factory=list)
