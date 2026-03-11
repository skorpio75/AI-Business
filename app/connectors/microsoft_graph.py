from datetime import datetime, timezone
from typing import Any, Optional
from urllib import parse

from app.connectors.http import ConnectorHttpError, get_json
from app.models.connectors import CalendarEvent, CalendarSyncCursor, ConnectorHealth, InboxMessage, InboxSyncCursor


class MicrosoftGraphInboxConnector:
    connector_id = "microsoft-graph-inbox"
    base_url = "https://graph.microsoft.com/v1.0"

    def __init__(self, access_token: Optional[str]) -> None:
        self.access_token = access_token

    def healthcheck(self, account_id: str) -> ConnectorHealth:
        if not self.access_token:
            return ConnectorHealth(
                connector_id=self.connector_id,
                status="degraded",
                detail="Microsoft Graph inbox connector is selected but MICROSOFT_GRAPH_ACCESS_TOKEN is not configured.",
            )
        try:
            get_json(
                url=f"{self.base_url}/{self._user_path(account_id)}/mailFolders/inbox",
                headers=self._headers(),
                params={"$select": "id,displayName"},
            )
        except ConnectorHttpError as exc:
            return ConnectorHealth(connector_id=self.connector_id, status="error", detail=str(exc))
        return ConnectorHealth(
            connector_id=self.connector_id,
            status="ok",
            detail=f"Microsoft Graph mailbox connected for {account_id}.",
        )

    def list_messages(
        self,
        *,
        account_id: str,
        since: datetime | None = None,
        folder: str = "inbox",
        limit: int = 50,
    ) -> list[InboxMessage]:
        if not self.access_token:
            return []

        folder_name = folder if folder and folder != "inbox" else "inbox"
        params = {
            "$top": max(1, min(limit, 100)),
            "$orderby": "receivedDateTime desc",
            "$select": "id,conversationId,subject,bodyPreview,from,toRecipients,receivedDateTime,isRead,categories,parentFolderId,webLink",
        }
        if since:
            params["$filter"] = f"receivedDateTime ge {since.astimezone(timezone.utc).isoformat()}"

        payload = get_json(
            url=f"{self.base_url}/{self._user_path(account_id)}/mailFolders/{parse.quote(folder_name, safe='')}/messages",
            headers=self._headers(),
            params=params,
        )
        return [self._normalize_message(account_id=account_id, payload=item) for item in payload.get("value", [])]

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

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.access_token}"}

    def _user_path(self, account_id: str) -> str:
        return "me" if account_id == "me" else f"users/{parse.quote(account_id, safe='')}"

    def _normalize_message(self, *, account_id: str, payload: dict[str, Any]) -> InboxMessage:
        sender = ((payload.get("from") or {}).get("emailAddress") or {}).get("address", "unknown")
        recipients = [
            ((recipient.get("emailAddress") or {}).get("address", ""))
            for recipient in payload.get("toRecipients", []) or []
            if (recipient.get("emailAddress") or {}).get("address")
        ]
        return InboxMessage(
            message_id=payload.get("id", ""),
            thread_id=payload.get("conversationId"),
            account_id=account_id,
            folder="inbox",
            direction="inbound",
            sender=sender,
            recipients=recipients,
            subject=payload.get("subject") or "(no subject)",
            body_text=payload.get("bodyPreview") or "",
            received_at=self._parse_datetime(payload.get("receivedDateTime")),
            is_unread=not payload.get("isRead", False),
            labels=[str(item) for item in payload.get("categories", []) or []],
            metadata={
                "provider": self.connector_id,
                "parent_folder_id": str(payload.get("parentFolderId", "")),
                "web_link": str(payload.get("webLink", "")),
            },
        )

    def _parse_datetime(self, value: str | None) -> datetime:
        if not value:
            return datetime.now(timezone.utc)
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)


class MicrosoftGraphCalendarConnector:
    connector_id = "microsoft-graph-calendar"
    base_url = "https://graph.microsoft.com/v1.0"

    def __init__(self, access_token: Optional[str], principal_id: str = "me") -> None:
        self.access_token = access_token
        self.principal_id = principal_id

    def healthcheck(self, calendar_id: str) -> ConnectorHealth:
        if not self.access_token:
            return ConnectorHealth(
                connector_id=self.connector_id,
                status="degraded",
                detail="Microsoft Graph calendar connector is selected but MICROSOFT_GRAPH_ACCESS_TOKEN is not configured.",
            )
        path = (
            f"{self._principal_path()}/calendar"
            if calendar_id == "primary"
            else f"{self._principal_path()}/calendars/{parse.quote(calendar_id, safe='')}"
        )
        try:
            get_json(url=f"{self.base_url}/{path}", headers=self._headers())
        except ConnectorHttpError as exc:
            return ConnectorHealth(connector_id=self.connector_id, status="error", detail=str(exc))
        return ConnectorHealth(
            connector_id=self.connector_id,
            status="ok",
            detail=f"Microsoft Graph calendar connected for {calendar_id}.",
        )

    def list_events(
        self,
        *,
        calendar_id: str,
        start_at: datetime,
        end_at: datetime,
    ) -> list[CalendarEvent]:
        if not self.access_token:
            return []

        path = (
            f"{self._principal_path()}/calendarView"
            if calendar_id == "primary"
            else f"{self._principal_path()}/calendars/{parse.quote(calendar_id, safe='')}/calendarView"
        )
        payload = get_json(
            url=f"{self.base_url}/{path}",
            headers=self._headers(),
            params={
                "startDateTime": start_at.astimezone(timezone.utc).isoformat(),
                "endDateTime": end_at.astimezone(timezone.utc).isoformat(),
                "$top": 250,
                "$orderby": "start/dateTime",
                "$select": "id,subject,start,end,organizer,attendees,location,bodyPreview,responseStatus,isAllDay,webLink",
            },
        )
        return [self._normalize_event(calendar_id=calendar_id, payload=item) for item in payload.get("value", [])]

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

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.access_token}", "Prefer": 'outlook.timezone="UTC"'}

    def _principal_path(self) -> str:
        return "me" if self.principal_id == "me" else f"users/{parse.quote(self.principal_id, safe='')}"

    def _normalize_event(self, *, calendar_id: str, payload: dict[str, Any]) -> CalendarEvent:
        response = (payload.get("responseStatus") or {}).get("response", "accepted")
        normalized_status = response if response in {"accepted", "tentative", "declined", "needs_action"} else "accepted"
        return CalendarEvent(
            event_id=payload.get("id", ""),
            calendar_id=calendar_id,
            title=payload.get("subject") or "(untitled event)",
            start_at=self._parse_datetime((payload.get("start") or {}).get("dateTime")),
            end_at=self._parse_datetime((payload.get("end") or {}).get("dateTime")),
            organizer=((payload.get("organizer") or {}).get("emailAddress") or {}).get("address"),
            attendees=[
                ((attendee.get("emailAddress") or {}).get("address", ""))
                for attendee in payload.get("attendees", []) or []
                if (attendee.get("emailAddress") or {}).get("address")
            ],
            location=((payload.get("location") or {}).get("displayName")),
            description=payload.get("bodyPreview"),
            response_status=normalized_status,
            is_all_day=bool(payload.get("isAllDay", False)),
            metadata={"provider": self.connector_id, "web_link": str(payload.get("webLink", ""))},
        )

    def _parse_datetime(self, value: str | None) -> datetime:
        if not value:
            return datetime.now(timezone.utc)
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
