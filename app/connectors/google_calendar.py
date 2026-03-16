# Copyright (c) Dario Pizzolante
from datetime import date, datetime, timezone
from typing import Any, Optional
from urllib import parse

from app.connectors.http import ConnectorHttpError, get_json
from app.models.connectors import CalendarEvent, CalendarSyncCursor, ConnectorHealth


class GoogleCalendarConnector:
    connector_id = "google-calendar"
    base_url = "https://www.googleapis.com/calendar/v3"

    def __init__(self, access_token: Optional[str]) -> None:
        self.access_token = access_token

    def healthcheck(self, calendar_id: str) -> ConnectorHealth:
        if not self.access_token:
            return ConnectorHealth(
                connector_id=self.connector_id,
                status="degraded",
                detail="Google Calendar connector is selected but GOOGLE_ACCESS_TOKEN is not configured.",
            )
        try:
            get_json(
                url=f"{self.base_url}/calendars/{parse.quote(calendar_id, safe='')}",
                headers=self._headers(),
            )
        except ConnectorHttpError as exc:
            return ConnectorHealth(connector_id=self.connector_id, status="error", detail=str(exc))
        return ConnectorHealth(
            connector_id=self.connector_id,
            status="ok",
            detail=f"Google Calendar connected for {calendar_id}.",
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

        payload = get_json(
            url=f"{self.base_url}/calendars/{parse.quote(calendar_id, safe='')}/events",
            headers=self._headers(),
            params={
                "timeMin": start_at.astimezone(timezone.utc).isoformat(),
                "timeMax": end_at.astimezone(timezone.utc).isoformat(),
                "singleEvents": "true",
                "orderBy": "startTime",
                "maxResults": 250,
            },
        )
        events: list[CalendarEvent] = []
        for item in payload.get("items", []):
            normalized = self._normalize_event(calendar_id=calendar_id, payload=item)
            if normalized is not None:
                events.append(normalized)
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

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.access_token}"}

    def _normalize_event(self, *, calendar_id: str, payload: dict[str, Any]) -> CalendarEvent | None:
        start_at, is_all_day = self._parse_event_time(payload.get("start", {}))
        end_at, _ = self._parse_event_time(payload.get("end", {}))
        if start_at is None or end_at is None:
            return None

        attendees = payload.get("attendees", []) or []
        self_attendee = next((item for item in attendees if item.get("self")), {})
        response_status = self_attendee.get("responseStatus", "accepted")
        normalized_status = response_status if response_status in {"accepted", "tentative", "declined", "needs_action"} else "accepted"

        return CalendarEvent(
            event_id=payload.get("id", ""),
            calendar_id=calendar_id,
            title=payload.get("summary", "(untitled event)"),
            start_at=start_at,
            end_at=end_at,
            organizer=(payload.get("organizer") or {}).get("email"),
            attendees=[item.get("email", "") for item in attendees if item.get("email")],
            location=payload.get("location"),
            description=payload.get("description"),
            response_status=normalized_status,
            is_all_day=is_all_day,
            metadata={"provider": self.connector_id, "status": payload.get("status", "")},
        )

    def _parse_event_time(self, value: dict[str, Any]) -> tuple[datetime | None, bool]:
        if "dateTime" in value:
            return self._parse_datetime(value["dateTime"]), False
        if "date" in value:
            parsed = datetime.combine(date.fromisoformat(value["date"]), datetime.min.time(), tzinfo=timezone.utc)
            return parsed, True
        return None, False

    def _parse_datetime(self, value: str) -> datetime:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
