# Copyright (c) Dario Pizzolante
import base64
from datetime import datetime, timezone
from typing import Any, Optional
from urllib import parse

from app.connectors.http import ConnectorHttpError, get_json
from app.models.connectors import ConnectorHealth, InboxMessage, InboxSyncCursor


class GmailInboxConnector:
    connector_id = "gmail"
    base_url = "https://gmail.googleapis.com/gmail/v1"

    def __init__(self, access_token: Optional[str]) -> None:
        self.access_token = access_token

    def healthcheck(self, account_id: str) -> ConnectorHealth:
        if not self.access_token:
            return ConnectorHealth(
                connector_id=self.connector_id,
                status="degraded",
                detail="Gmail connector is selected but GOOGLE_ACCESS_TOKEN is not configured.",
            )
        try:
            get_json(
                url=f"{self.base_url}/users/{parse.quote(account_id, safe='')}/profile",
                headers=self._headers(),
            )
        except ConnectorHttpError as exc:
            return ConnectorHealth(connector_id=self.connector_id, status="error", detail=str(exc))

        return ConnectorHealth(connector_id=self.connector_id, status="ok", detail=f"Gmail connected for {account_id}.")

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

        label_ids = ["INBOX"] if folder.lower() == "inbox" else None
        query = f"after:{int(since.timestamp())}" if since else None
        payload = get_json(
            url=f"{self.base_url}/users/{parse.quote(account_id, safe='')}/messages",
            headers=self._headers(),
            params={
                "maxResults": max(1, min(limit, 100)),
                "labelIds": label_ids,
                "q": query,
            },
        )
        messages: list[InboxMessage] = []
        for item in payload.get("messages", []):
            detail = get_json(
                url=f"{self.base_url}/users/{parse.quote(account_id, safe='')}/messages/{item['id']}",
                headers=self._headers(),
                params={"format": "full"},
            )
            normalized = self._normalize_message(account_id=account_id, payload=detail)
            if normalized is not None:
                messages.append(normalized)
        return messages

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
        raise NotImplementedError("gmail_reply_not_implemented")

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.access_token}"}

    def _normalize_message(self, *, account_id: str, payload: dict[str, Any]) -> InboxMessage | None:
        headers = {item.get("name", "").lower(): item.get("value", "") for item in payload.get("payload", {}).get("headers", [])}
        internal_date = payload.get("internalDate")
        if internal_date is None:
            return None

        try:
            received_at = datetime.fromtimestamp(int(internal_date) / 1000, tz=timezone.utc)
        except (TypeError, ValueError):
            return None

        labels = [str(label) for label in payload.get("labelIds", [])]
        recipients = self._split_addresses(headers.get("to", ""))
        sender = headers.get("from", "unknown")
        body_text = self._extract_body(payload.get("payload", {})) or payload.get("snippet", "")

        return InboxMessage(
            message_id=payload.get("id", ""),
            thread_id=payload.get("threadId"),
            account_id=account_id,
            folder="inbox",
            direction="inbound",
            sender=sender,
            recipients=recipients,
            subject=headers.get("subject", "(no subject)"),
            body_text=body_text,
            received_at=received_at,
            is_unread="UNREAD" in labels,
            labels=labels,
            metadata={"provider": self.connector_id},
        )

    def _extract_body(self, payload: dict[str, Any]) -> str:
        body = self._decode_body(payload.get("body", {}))
        if body:
            return body

        for part in payload.get("parts", []) or []:
            mime_type = part.get("mimeType", "")
            if mime_type == "text/plain":
                text = self._decode_body(part.get("body", {}))
                if text:
                    return text
            nested = self._extract_body(part)
            if nested:
                return nested
        return ""

    def _decode_body(self, body: dict[str, Any]) -> str:
        data = body.get("data")
        if not data:
            return ""
        padding = "=" * (-len(data) % 4)
        try:
            return base64.urlsafe_b64decode(data + padding).decode("utf-8", errors="replace")
        except (ValueError, TypeError):
            return ""

    def _split_addresses(self, value: str) -> list[str]:
        return [item.strip() for item in value.split(",") if item.strip()]
