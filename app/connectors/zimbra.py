# Copyright (c) Dario Pizzolante
import base64
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Iterable, Optional
from urllib import parse

from app.connectors.calendar import CalendarConnector
from app.connectors.http import ConnectorHttpError, get_json
from app.connectors.inbox import InboxConnector
from app.connectors.tasks import TaskConnector
from app.models.connectors import (
    CalendarEvent,
    CalendarSyncCursor,
    ConnectorHealth,
    InboxMessage,
    InboxSyncCursor,
    TaskSyncCursor,
    TodoTask,
)


class _ZimbraConnectorBase:
    provider_id = "zimbra"

    def __init__(
        self,
        *,
        base_url: Optional[str],
        access_token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        principal_id: str = "me",
        request_timeout: int = 10,
    ) -> None:
        self.base_url = base_url.rstrip("/") if base_url else None
        self.access_token = access_token
        self.username = username
        self.password = password
        self.principal_id = principal_id
        self.request_timeout = request_timeout

    def _configured(self) -> tuple[bool, str]:
        if not self.base_url:
            return False, "Zimbra connector is selected but ZIMBRA_BASE_URL is not configured."
        if self.access_token:
            return True, ""
        if self.username and self.password:
            return True, ""
        return False, "Zimbra connector is selected but no auth is configured. Set ZIMBRA_ACCESS_TOKEN or ZIMBRA_USERNAME/ZIMBRA_PASSWORD."

    def _headers(self) -> dict[str, str]:
        if self.username and self.password and not self.access_token:
            raw = f"{self.username}:{self.password}".encode("utf-8")
            return {"Authorization": f"Basic {base64.b64encode(raw).decode('ascii')}"}
        return {}

    def _auth_params(self) -> dict[str, str]:
        if self.access_token:
            return {"auth": "qp", "zauthtoken": self.access_token}
        if self.username and self.password:
            return {"auth": "ba"}
        return {}

    def _home_url(self, account_id: str, folder_path: str) -> str:
        if not self.base_url:
            raise ConnectorHttpError("Zimbra connector is not configured.")
        encoded_account = parse.quote(account_id, safe="@._+-")
        encoded_path = "/".join(parse.quote(part, safe="") for part in folder_path.split("/") if part)
        return f"{self.base_url}/home/{encoded_account}/{encoded_path}"

    def _get_folder_payload(
        self,
        *,
        account_id: str,
        folder_path: str,
        extra_params: Optional[dict[str, Any]] = None,
    ) -> Any:
        configured, detail = self._configured()
        if not configured:
            raise ConnectorHttpError(detail)
        params = {"fmt": "json", **self._auth_params(), **(extra_params or {})}
        return get_json(
            url=self._home_url(account_id, folder_path),
            headers=self._headers(),
            params=params,
            timeout=self.request_timeout,
        )

    def _iter_dicts(self, payload: Any) -> Iterable[dict[str, Any]]:
        if isinstance(payload, dict):
            yield payload
            for value in payload.values():
                yield from self._iter_dicts(value)
        elif isinstance(payload, list):
            for item in payload:
                yield from self._iter_dicts(item)

    def _lookup(self, payload: dict[str, Any], *keys: str) -> Any:
        attrs = payload.get("_attrs")
        for key in keys:
            if key in payload:
                return payload[key]
            if isinstance(attrs, dict) and key in attrs:
                return attrs[key]
        return None

    def _as_text(self, value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, str):
            text = value.strip()
            return text or None
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, dict):
            for key in ("_content", "content", "value", "email", "address", "a", "name", "d"):
                nested = self._as_text(value.get(key))
                if nested:
                    return nested
        if isinstance(value, list):
            parts = [part for part in (self._as_text(item) for item in value) if part]
            if parts:
                return ", ".join(parts)
        return None

    def _parse_datetime(self, value: Any) -> datetime | None:
        if value is None or value == "":
            return None
        if isinstance(value, datetime):
            return value.astimezone(timezone.utc) if value.tzinfo else value.replace(tzinfo=timezone.utc)
        if isinstance(value, (int, float)):
            timestamp = float(value)
            if timestamp > 10_000_000_000:
                timestamp /= 1000
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)

        text = str(value).strip()
        if not text:
            return None
        if text.isdigit():
            return self._parse_datetime(int(text))
        if text.endswith("Z") and "T" in text:
            try:
                return datetime.fromisoformat(text[:-1] + "+00:00").astimezone(timezone.utc)
            except ValueError:
                pass
        try:
            parsed = datetime.fromisoformat(text)
            return parsed.astimezone(timezone.utc) if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            pass
        for pattern in ("%Y%m%dT%H%M%SZ", "%Y%m%dT%H%M%S", "%Y%m%d", "%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y"):
            try:
                parsed = datetime.strptime(text, pattern)
                return parsed.replace(tzinfo=timezone.utc)
            except ValueError:
                continue
        try:
            parsed = parsedate_to_datetime(text)
            return parsed.astimezone(timezone.utc) if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except (TypeError, ValueError):
            return None

    def _normalize_response_status(self, value: Any) -> str:
        normalized = (self._as_text(value) or "").strip().lower()
        mapping = {
            "accepted": "accepted",
            "ac": "accepted",
            "tentative": "tentative",
            "te": "tentative",
            "declined": "declined",
            "de": "declined",
            "needs_action": "needs_action",
            "needs-action": "needs_action",
            "ne": "needs_action",
        }
        return mapping.get(normalized, "accepted")

    def _normalize_task_status(self, value: Any, *, completed_at: datetime | None = None) -> str:
        if completed_at is not None:
            return "completed"
        normalized = (self._as_text(value) or "").strip().lower()
        mapping = {
            "inprogress": "in_progress",
            "in_progress": "in_progress",
            "in progress": "in_progress",
            "started": "in_progress",
            "waiting": "waiting",
            "deferred": "deferred",
            "completed": "completed",
            "done": "completed",
            "not_started": "not_started",
            "not started": "not_started",
            "new": "not_started",
        }
        return mapping.get(normalized, "not_started")

    def _normalize_task_priority(self, value: Any) -> str:
        normalized = (self._as_text(value) or "").strip().lower()
        mapping = {
            "1": "high",
            "2": "normal",
            "3": "low",
            "high": "high",
            "normal": "normal",
            "medium": "normal",
            "low": "low",
        }
        return mapping.get(normalized, "normal")


class ZimbraInboxConnector(_ZimbraConnectorBase, InboxConnector):
    connector_id = "zimbra-inbox"

    def healthcheck(self, account_id: str) -> ConnectorHealth:
        configured, detail = self._configured()
        if not configured:
            return ConnectorHealth(connector_id=self.connector_id, status="degraded", detail=detail)
        try:
            self._get_folder_payload(account_id=account_id, folder_path="inbox")
        except ConnectorHttpError as exc:
            return ConnectorHealth(connector_id=self.connector_id, status="error", detail=str(exc))
        return ConnectorHealth(
            connector_id=self.connector_id,
            status="ok",
            detail=f"Zimbra inbox connected for {account_id}.",
        )

    def list_messages(
        self,
        *,
        account_id: str,
        since: datetime | None = None,
        folder: str = "inbox",
        limit: int = 50,
    ) -> list[InboxMessage]:
        configured, _ = self._configured()
        if not configured:
            return []
        payload = self._get_folder_payload(account_id=account_id, folder_path=folder or "inbox")
        messages: list[InboxMessage] = []
        seen: set[str] = set()
        for record in self._iter_dicts(payload):
            message_id = self._as_text(self._lookup(record, "id"))
            received_at = self._parse_datetime(self._lookup(record, "d", "date", "receivedDateTime"))
            subject = self._as_text(self._lookup(record, "su", "subject"))
            sender = self._as_text(self._lookup(record, "fr", "from", "sender"))
            if not message_id or not received_at or not (subject or sender):
                continue
            if message_id in seen:
                continue
            if since and received_at < since.astimezone(timezone.utc):
                continue
            recipients = self._extract_recipients(record)
            labels = self._extract_labels(record)
            flags = (self._as_text(self._lookup(record, "f", "flags")) or "").lower()
            messages.append(
                InboxMessage(
                    message_id=message_id,
                    thread_id=self._as_text(self._lookup(record, "cid", "convId", "conversationId")),
                    account_id=account_id,
                    folder=folder if folder in {"inbox", "sent", "archive"} else "inbox",
                    direction="inbound",
                    sender=sender or "unknown",
                    recipients=recipients,
                    subject=subject or "(no subject)",
                    body_text=self._as_text(self._lookup(record, "desc", "summary", "body", "bodyPreview")) or "",
                    received_at=received_at,
                    is_unread="u" in flags if flags else True,
                    labels=labels,
                    metadata={"provider": self.connector_id},
                )
            )
            seen.add(message_id)
        messages.sort(key=lambda item: item.received_at, reverse=True)
        return messages[: max(1, min(limit, 100))]

    def pull_incremental(
        self,
        *,
        account_id: str,
        cursor: InboxSyncCursor | None = None,
        limit: int = 100,
    ) -> tuple[list[InboxMessage], InboxSyncCursor]:
        since = cursor.synced_at if cursor and cursor.synced_at else None
        messages = self.list_messages(account_id=account_id, since=since, limit=limit)
        latest = max((message.received_at for message in messages), default=None)
        return messages, InboxSyncCursor(
            account_id=account_id,
            cursor=latest.isoformat() if latest else (cursor.cursor if cursor else None),
            synced_at=datetime.now(timezone.utc),
        )

    def reply_to_message(
        self,
        *,
        account_id: str,
        message_id: str,
        reply_body: str,
    ) -> None:
        del account_id, message_id, reply_body
        raise NotImplementedError("zimbra_reply_not_implemented")

    def _extract_recipients(self, record: dict[str, Any]) -> list[str]:
        recipients: list[str] = []
        for value in record.get("e", []) or []:
            if not isinstance(value, dict):
                continue
            address = self._as_text(value.get("a") or value.get("email") or value.get("address"))
            if address:
                recipients.append(address)
        fallback = self._as_text(self._lookup(record, "to", "recipients"))
        if fallback:
            recipients.extend([item.strip() for item in fallback.split(",") if item.strip()])
        return list(dict.fromkeys(recipients))

    def _extract_labels(self, record: dict[str, Any]) -> list[str]:
        labels: list[str] = []
        for key in ("tn", "tags", "l", "folder"):
            value = self._lookup(record, key)
            if isinstance(value, list):
                labels.extend(item for item in (self._as_text(entry) for entry in value) if item)
            else:
                text = self._as_text(value)
                if text:
                    labels.append(text)
        return list(dict.fromkeys(labels))


class ZimbraCalendarConnector(_ZimbraConnectorBase, CalendarConnector):
    connector_id = "zimbra-calendar"

    def healthcheck(self, calendar_id: str) -> ConnectorHealth:
        configured, detail = self._configured()
        if not configured:
            return ConnectorHealth(connector_id=self.connector_id, status="degraded", detail=detail)
        try:
            self._get_folder_payload(account_id=self._principal_for_healthcheck(), folder_path=self._calendar_path(calendar_id))
        except ConnectorHttpError as exc:
            return ConnectorHealth(connector_id=self.connector_id, status="error", detail=str(exc))
        return ConnectorHealth(
            connector_id=self.connector_id,
            status="ok",
            detail=f"Zimbra calendar connected for {calendar_id}.",
        )

    def list_events(
        self,
        *,
        calendar_id: str,
        start_at: datetime,
        end_at: datetime,
    ) -> list[CalendarEvent]:
        configured, _ = self._configured()
        if not configured:
            return []
        account_id = self._principal_for_healthcheck()
        payload = self._get_folder_payload(
            account_id=account_id,
            folder_path=self._calendar_path(calendar_id),
            extra_params={
                "start": int(start_at.astimezone(timezone.utc).timestamp() * 1000),
                "end": int(end_at.astimezone(timezone.utc).timestamp() * 1000),
            },
        )
        events: list[CalendarEvent] = []
        seen: set[str] = set()
        for record in self._iter_dicts(payload):
            event_id = self._as_text(self._lookup(record, "id", "uid"))
            start_value = self._parse_datetime(self._lookup(record, "s", "start", "startTime", "startDate"))
            end_value = self._parse_datetime(self._lookup(record, "e", "end", "endTime", "endDate"))
            title = self._as_text(self._lookup(record, "name", "su", "subject", "summary"))
            if not event_id or not start_value or not title:
                continue
            if event_id in seen:
                continue
            resolved_end = end_value or start_value
            if resolved_end < start_at.astimezone(timezone.utc) or start_value > end_at.astimezone(timezone.utc):
                continue
            events.append(
                CalendarEvent(
                    event_id=event_id,
                    calendar_id=calendar_id,
                    title=title,
                    start_at=start_value,
                    end_at=resolved_end,
                    organizer=self._as_text(self._lookup(record, "or", "organizer", "fr", "from")),
                    attendees=self._extract_attendees(record),
                    location=self._as_text(self._lookup(record, "loc", "location")),
                    description=self._as_text(self._lookup(record, "desc", "description")),
                    response_status=self._normalize_response_status(
                        self._lookup(record, "ptst", "partStat", "responseStatus", "status")
                    ),
                    is_all_day=bool(self._lookup(record, "allDay", "isAllDay"))
                    or self._looks_like_date_only(self._lookup(record, "s", "start", "startDate")),
                    metadata={"provider": self.connector_id},
                )
            )
            seen.add(event_id)
        events.sort(key=lambda item: item.start_at)
        return events

    def pull_incremental(
        self,
        *,
        calendar_id: str,
        cursor: CalendarSyncCursor | None = None,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
    ) -> tuple[list[CalendarEvent], CalendarSyncCursor]:
        start = start_at or cursor.synced_at or datetime.now(timezone.utc)
        finish = end_at or start
        events = self.list_events(calendar_id=calendar_id, start_at=start, end_at=finish)
        latest = max((event.end_at for event in events), default=None)
        return events, CalendarSyncCursor(
            calendar_id=calendar_id,
            cursor=latest.isoformat() if latest else (cursor.cursor if cursor else None),
            synced_at=datetime.now(timezone.utc),
        )

    def _calendar_path(self, calendar_id: str) -> str:
        return "calendar" if calendar_id == "primary" else calendar_id

    def _principal_for_healthcheck(self) -> str:
        return self.principal_id

    def _extract_attendees(self, record: dict[str, Any]) -> list[str]:
        attendees: list[str] = []
        for key in ("at", "attendees", "e"):
            value = record.get(key)
            if not isinstance(value, list):
                continue
            for item in value:
                if not isinstance(item, dict):
                    continue
                address = self._as_text(item.get("a") or item.get("email") or item.get("address"))
                if address:
                    attendees.append(address)
        return list(dict.fromkeys(attendees))

    def _looks_like_date_only(self, value: Any) -> bool:
        text = self._as_text(value) or ""
        return len(text) == 8 and text.isdigit()


class ZimbraTaskConnector(_ZimbraConnectorBase, TaskConnector):
    connector_id = "zimbra-tasks"

    def healthcheck(self, list_id: str) -> ConnectorHealth:
        configured, detail = self._configured()
        if not configured:
            return ConnectorHealth(connector_id=self.connector_id, status="degraded", detail=detail)
        try:
            self._get_folder_payload(account_id=self._principal_for_healthcheck(), folder_path=self._task_path(list_id))
        except ConnectorHttpError as exc:
            return ConnectorHealth(connector_id=self.connector_id, status="error", detail=str(exc))
        return ConnectorHealth(
            connector_id=self.connector_id,
            status="ok",
            detail=f"Zimbra tasks connected for {list_id}.",
        )

    def list_tasks(
        self,
        *,
        list_id: str,
        since: datetime | None = None,
        limit: int = 50,
        include_completed: bool = False,
    ) -> list[TodoTask]:
        configured, _ = self._configured()
        if not configured:
            return []
        payload = self._get_folder_payload(
            account_id=self._principal_for_healthcheck(),
            folder_path=self._task_path(list_id),
        )
        tasks: list[TodoTask] = []
        seen: set[str] = set()
        for record in self._iter_dicts(payload):
            task_id = self._as_text(self._lookup(record, "id", "uid"))
            title = self._as_text(self._lookup(record, "name", "su", "subject", "summary"))
            due_at = self._parse_datetime(self._lookup(record, "due", "e", "end", "endDate"))
            completed_at = self._parse_datetime(self._lookup(record, "completed", "compDate"))
            if not task_id or not title:
                continue
            if task_id in seen:
                continue
            if since:
                comparison = completed_at or due_at
                if comparison and comparison < since.astimezone(timezone.utc):
                    continue
            status = self._normalize_task_status(self._lookup(record, "status", "percentComplete"), completed_at=completed_at)
            if status == "completed" and not include_completed:
                continue
            tasks.append(
                TodoTask(
                    task_id=task_id,
                    list_id=list_id,
                    title=title,
                    body_text=self._as_text(self._lookup(record, "desc", "description", "notes")),
                    due_at=due_at,
                    completed_at=completed_at,
                    status=status,
                    priority=self._normalize_task_priority(self._lookup(record, "priority", "p")),
                    web_link=self._as_text(self._lookup(record, "webLink", "url")),
                    metadata={"provider": self.connector_id},
                )
            )
            seen.add(task_id)
        tasks.sort(key=lambda item: (item.completed_at is not None, item.due_at or datetime.max.replace(tzinfo=timezone.utc), item.title.lower()))
        return tasks[: max(1, min(limit, 100))]

    def pull_incremental(
        self,
        *,
        list_id: str,
        cursor: TaskSyncCursor | None = None,
        limit: int = 100,
        include_completed: bool = False,
    ) -> tuple[list[TodoTask], TaskSyncCursor]:
        since = cursor.synced_at if cursor and cursor.synced_at else None
        tasks = self.list_tasks(list_id=list_id, since=since, limit=limit, include_completed=include_completed)
        latest = max((task.completed_at or task.due_at for task in tasks if task.completed_at or task.due_at), default=None)
        return tasks, TaskSyncCursor(
            list_id=list_id,
            cursor=latest.isoformat() if latest else (cursor.cursor if cursor else None),
            synced_at=datetime.now(timezone.utc),
        )

    def _task_path(self, list_id: str) -> str:
        return "Tasks" if list_id in {"primary", "default"} else list_id

    def _principal_for_healthcheck(self) -> str:
        return self.principal_id
