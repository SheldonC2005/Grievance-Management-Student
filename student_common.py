import time
from typing import Any

import streamlit as st

from config.settings import get_settings
from repositories.grievance_repository import GrievanceRepository
from repositories.notification_repository import NotificationRepository
from supabase_client import authenticated_supabase, require_demo_session


def require_authenticated_page() -> None:
    try:
        require_demo_session(st.session_state)
    except RuntimeError:
        st.warning("Please sign in with an approved student account to open this page.")
        st.page_link("student_app.py", label="Return to sign in")
        st.stop()


def client() -> Any:
    get_settings()
    require_demo_session(st.session_state)
    return authenticated_supabase(st.session_state["session"])


def auto_refresh(interval_seconds: int = 20) -> None:
    last_refresh = st.session_state.get("last_refresh")
    now = time.monotonic()
    if last_refresh is None:
        st.session_state["last_refresh"] = now
        return
    if now - last_refresh >= interval_seconds:
        st.session_state["last_refresh"] = now
        st.rerun()


def current_user_id() -> str:
    require_demo_session(st.session_state)
    return str(st.session_state["user"].id)


def grievance_repository() -> GrievanceRepository:
    return GrievanceRepository(client())


def notification_repository() -> NotificationRepository:
    return NotificationRepository(client())