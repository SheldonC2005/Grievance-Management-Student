from typing import Any

import streamlit as st

from config.settings import get_settings
from repositories.grievance_repository import GrievanceRepository
from repositories.notification_repository import NotificationRepository
from services.supabase_client import get_supabase


def client() -> Any:
    get_settings()
    return get_supabase()


def current_user_id() -> str:
    return str(st.session_state["user"].id)


def grievance_repository() -> GrievanceRepository:
    return GrievanceRepository(client())


def notification_repository() -> NotificationRepository:
    return NotificationRepository(client())