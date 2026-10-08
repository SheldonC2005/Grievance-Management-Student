from typing import Any


class StudentRepository:
    def __init__(self, client: Any) -> None:
        self.client = client

    def get_by_auth_user(self, user_id: str) -> dict[str, Any] | None:
        result = self.client.table("students").select("*").eq("auth_user_id", user_id).maybe_single().execute()
        return result.data

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.client.table("students").insert(payload).execute().data[0]

    def update_profile(self, user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        allowed = {key: value for key, value in payload.items() if key in {"name", "phone", "department", "programme", "year", "semester"}}
        return self.client.table("students").update(allowed).eq("auth_user_id", user_id).execute().data[0]

    def email_for_student_id(self, student_id: str) -> str | None:
        result = self.client.rpc("resolve_student_email", {"p_student_id": student_id}).execute()
        return result.data