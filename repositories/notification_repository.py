from typing import Any


class NotificationRepository:
    def __init__(self, client: Any) -> None:
        self.client = client

    def list(self) -> list[dict[str, Any]]:
        return self.client.table("notifications").select("*").order("created_at", desc=True).execute().data or []

    def unread_count(self) -> int:
        return len(self.client.table("notifications").select("id").eq("is_read", False).execute().data or [])

    def mark_read(self, notification_id: str) -> None:
        self.client.table("notifications").update({"is_read": True}).eq("id", notification_id).execute()