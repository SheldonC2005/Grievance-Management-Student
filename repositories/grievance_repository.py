from typing import Any


class GrievanceRepository:
    def __init__(self, client: Any) -> None:
        self.client = client

    def categories(self) -> list[dict[str, Any]]:
        return self.client.table("grievance_categories").select("id,name,description").eq("is_active", True).order("name").execute().data or []

    def list_for_student(self, search: str = "", status: str | None = None, category_id: str | None = None) -> list[dict[str, Any]]:
        query = self.client.table("grievances").select("*, grievance_categories(name)").order("created_at", desc=True)
        if search:
            query = query.ilike("title", f"%{search}%")
        if status:
            query = query.eq("status", status)
        if category_id:
            query = query.eq("category_id", category_id)
        return query.execute().data or []

    def get(self, grievance_id: str) -> dict[str, Any] | None:
        result = self.client.table("grievances").select("*, grievance_categories(name)").eq("id", grievance_id).maybe_single().execute()
        return result.data

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.client.table("grievances").insert(payload).execute().data[0]

    def add_initial_history(self, grievance_id: str, user_id: str) -> None:
        self.client.table("grievance_status_history").insert({"grievance_id": grievance_id, "new_status": "submitted", "changed_by": user_id, "remarks": "Grievance submitted"}).execute()

    def history(self, grievance_id: str) -> list[dict[str, Any]]:
        return self.client.table("grievance_status_history").select("*").eq("grievance_id", grievance_id).order("changed_at").execute().data or []

    def comments(self, grievance_id: str) -> list[dict[str, Any]]:
        return self.client.table("grievance_comments").select("*").eq("grievance_id", grievance_id).order("created_at").execute().data or []

    def attachments(self, grievance_id: str) -> list[dict[str, Any]]:
        return self.client.table("grievance_attachments").select("*").eq("grievance_id", grievance_id).order("created_at").execute().data or []

    def add_comment(self, grievance_id: str, user_id: str, comment: str) -> dict[str, Any]:
        return self.client.table("grievance_comments").insert({"grievance_id": grievance_id, "author_user_id": user_id, "author_role": "student", "comment": comment}).execute().data[0]