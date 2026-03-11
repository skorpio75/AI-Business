from datetime import datetime
from typing import Protocol

from app.models.connectors import ConnectorHealth, InboxMessage, InboxSyncCursor


class InboxConnector(Protocol):
    connector_id: str

    def healthcheck(self, account_id: str) -> ConnectorHealth:
        """Return the current connector status for the target mailbox."""

    def list_messages(
        self,
        *,
        account_id: str,
        since: datetime | None = None,
        folder: str = "inbox",
        limit: int = 50,
    ) -> list[InboxMessage]:
        """Return normalized inbox messages for workflow consumption."""

    def pull_incremental(
        self,
        *,
        account_id: str,
        cursor: InboxSyncCursor | None = None,
        limit: int = 100,
    ) -> tuple[list[InboxMessage], InboxSyncCursor]:
        """Return only new mailbox items since the last sync."""

    def reply_to_message(
        self,
        *,
        account_id: str,
        message_id: str,
        reply_body: str,
    ) -> None:
        """Send a reply to a source message when supported by the provider."""


class NullInboxConnector:
    connector_id = "null-inbox"

    def healthcheck(self, account_id: str) -> ConnectorHealth:
        return ConnectorHealth(
            connector_id=self.connector_id,
            status="degraded",
            detail=f"No inbox connector configured for {account_id}.",
        )

    def list_messages(
        self,
        *,
        account_id: str,
        since: datetime | None = None,
        folder: str = "inbox",
        limit: int = 50,
    ) -> list[InboxMessage]:
        return []

    def pull_incremental(
        self,
        *,
        account_id: str,
        cursor: InboxSyncCursor | None = None,
        limit: int = 100,
    ) -> tuple[list[InboxMessage], InboxSyncCursor]:
        return [], InboxSyncCursor(account_id=account_id)

    def reply_to_message(
        self,
        *,
        account_id: str,
        message_id: str,
        reply_body: str,
    ) -> None:
        raise NotImplementedError("inbox_reply_not_supported")
