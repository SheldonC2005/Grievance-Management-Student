from __future__ import annotations

from functools import lru_cache
from types import SimpleNamespace
from typing import Any

from supabase import Client, create_client

from config.settings import get_settings
from utils.validators import is_valid_student_id, normalize_student_id

DEMO_ACCOUNTS = {
    "24BCE1234": "abcd123",
    "24BCE5678": "abcd123",
}


@lru_cache(maxsize=1)
def get_supabase() -> Client:
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_key)


def _session_tokens(session: Any) -> tuple[str, str] | None:
    if session is None:
        return None
    access_token = getattr(session, "access_token", None)
    refresh_token = getattr(session, "refresh_token", None)
    if isinstance(session, dict):
        access_token = session.get("access_token", access_token)
        refresh_token = session.get("refresh_token", refresh_token)
    if not access_token or not refresh_token:
        return None
    return str(access_token), str(refresh_token)


def authenticated_supabase(session: Any) -> Client:
    tokens = _session_tokens(session)
    if tokens is None:
        raise RuntimeError("No authenticated Supabase session is available.")
    client = get_supabase()
    client.auth.set_session(*tokens)
    return client


def validate_demo_credentials(student_id: str, password: str) -> bool:
    normalized = normalize_student_id(student_id)
    if not is_valid_student_id(normalized):
        return False
    expected_password = DEMO_ACCOUNTS.get(normalized)
    if expected_password is None:
        return False
    return password == expected_password


def get_demo_student_record(student_id: str, client: Any | None = None) -> dict[str, Any] | None:
    normalized = normalize_student_id(student_id)
    if not is_valid_student_id(normalized) or normalized not in DEMO_ACCOUNTS:
        return None
    try:
        database = client or get_supabase()
        result = database.table("students").select("*").eq("student_id", normalized).maybe_single().execute()
        return result.data
    except Exception as error:
        raise RuntimeError("The shared Supabase student table could not be reached.") from error


def sign_in_demo_student(student_id: str, password: str) -> Any:
    normalized = normalize_student_id(student_id)
    if not validate_demo_credentials(normalized, password):
        raise ValueError("Invalid student ID or password for the approved demo accounts.")

    database = get_supabase()
    try:
        email_result = database.rpc("resolve_student_email", {"p_student_id": normalized}).execute()
    except Exception as error:
        raise RuntimeError("The shared Supabase student identity lookup could not be reached.") from error
    email = email_result.data
    if not email:
        raise ValueError("This approved demo student is not configured in the shared Supabase student table.")

    response = database.auth.sign_in_with_password({"email": email, "password": password})
    if not getattr(response, "user", None):
        raise ValueError("Supabase authentication failed for the approved demo account.")
    profile = get_demo_student_record(normalized, database)
    if not profile or profile.get("auth_user_id") != response.user.id:
        database.auth.sign_out()
        raise ValueError("The authenticated Supabase user is not linked to the approved student record.")
    return response


def clear_demo_session(session: dict[str, Any] | None = None) -> dict[str, Any]:
    if session is None:
        try:
            import streamlit as st

            session = st.session_state
        except Exception:
            return {}

    for key in ("session", "user", "student", "auth_session", "demo_session"):
        session.pop(key, None)
    return session


from collections.abc import Mapping

def require_demo_session(session: Any) -> Any:
    if not isinstance(session, Mapping):
        raise RuntimeError("No authenticated student session is available.")
    if "student" not in session or "user" not in session:
        raise RuntimeError("No authenticated student session is available.")

    student = session["student"]
    user = session["user"]
    if not isinstance(student, dict):
        raise RuntimeError("The active session is not an authenticated demo student.")
    if student.get("student_id") not in DEMO_ACCOUNTS:
        raise RuntimeError("The active session is not an authenticated demo student.")
    if getattr(user, "id", None) != student.get("auth_user_id"):
        raise RuntimeError("Student session data does not match the authenticated demo account.")
    return session
