import logging

import streamlit as st

from components.ui import inject_styles
from config.settings import get_settings
from repositories.student_repository import StudentRepository
from services.auth_service import AuthService
from services.supabase_client import get_supabase
from utils.validators import is_valid_student_id, validate_email, validate_phone

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(page_title="VIT Student Grievance Portal", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")
inject_styles()


def clear_session() -> None:
    for key in ("session", "user", "student"):
        st.session_state.pop(key, None)


def show_auth_error(error: Exception, action: str) -> None:
    error_text = str(error).lower()
    if "getaddrinfo failed" in error_text or "connecterror" in error_text or "name or service not known" in error_text:
        st.error("Supabase cannot be reached. Check that SUPABASE_URL is the URL from Supabase Project Settings > API, then restart the app.")
        return
    if "already registered" in error_text or "duplicate" in error_text or "user already registered" in error_text:
        st.error("That Student ID or email is already registered.")
        return
    if "row-level security" in error_text or "42501" in error_text:
        st.error("Student profile creation is not configured in Supabase yet. Run sql/001_signup_profile_trigger.sql in the Supabase SQL editor, then restart this app.")
        return
    logger.exception("Student %s failed", action, exc_info=error)
    st.error(f"{action.title()} failed. Check your details and try again.")


def authenticate() -> bool:
    if "session" not in st.session_state:
        return False
    try:
        user = st.session_state["session"].user
        profile = StudentRepository(get_supabase()).get_by_auth_user(user.id)
        if not profile:
            clear_session()
            return False
        st.session_state["user"] = user
        st.session_state["student"] = profile
        return True
    except Exception:
        clear_session()
        return False


def login_form() -> None:
    st.markdown('<div class="portal-kicker">Vellore Institute of Technology</div><h1 class="portal-title">Student Grievance Portal</h1>', unsafe_allow_html=True)
    st.write("A secure channel to submit, track, and follow up on campus concerns.")
    login, signup = st.tabs(["Sign in", "Create account"])
    with login:
        with st.form("login"):
            student_id = st.text_input("Student ID", placeholder="24BCE1234").upper()
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign in", type="primary", use_container_width=True)
        if submitted:
            if not is_valid_student_id(student_id):
                st.error("Enter a valid Student ID such as 24BCE1234.")
            elif not password:
                st.error("Enter your password.")
            else:
                try:
                    response = AuthService(get_supabase(), get_settings().app_url).sign_in(student_id, password)
                    st.session_state["session"] = response
                    st.rerun()
                except Exception as error:
                    show_auth_error(error, "sign in")
    with signup:
        with st.form("signup"):
            student_id = st.text_input("Student ID", key="signup_id", placeholder="24BCE1234").upper()
            name = st.text_input("Full name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Create account", type="primary", use_container_width=True)
        if submitted:
            errors = []
            if not is_valid_student_id(student_id): errors.append("Student ID must match YY + 3 uppercase letters + 4 digits.")
            if len(name.strip()) < 2: errors.append("Enter your full name.")
            if not validate_email(email): errors.append("Enter a valid email address.")
            if not validate_phone(phone): errors.append("Enter a valid phone number.")
            if len(password) < 8: errors.append("Password must contain at least 8 characters.")
            if password != confirm: errors.append("Passwords do not match.")
            if errors:
                for error in errors: st.error(error)
            else:
                try:
                    response = AuthService(get_supabase(), get_settings().app_url).sign_up(student_id, name, email, phone, password)
                    if response.session:
                        st.session_state["session"] = response
                        st.rerun()
                    else:
                        st.success("Account created. Confirm your email, then sign in.")
                except Exception as error:
                    show_auth_error(error, "account creation")


def main() -> None:
    try:
        get_settings()
    except RuntimeError as error:
        st.error(str(error))
        st.info("Create a .env file from .env.example or configure Streamlit secrets.")
        st.stop()
    if not authenticate():
        login_form()
        return
    st.sidebar.markdown("### VIT Student Portal")
    st.sidebar.caption(st.session_state["student"]["name"])
    if st.sidebar.button("Log out", use_container_width=True):
        try: AuthService(get_supabase(), get_settings().app_url).sign_out()
        finally: clear_session(); st.rerun()
    st.sidebar.page_link("pages/1_Dashboard.py", label="Dashboard", icon="🏠")
    st.sidebar.page_link("pages/2_Submit_Grievance.py", label="Submit grievance", icon="＋")
    st.sidebar.page_link("pages/3_My_Grievances.py", label="My grievances", icon="▣")
    st.sidebar.page_link("pages/4_Notifications.py", label="Notifications", icon="🔔")
    st.sidebar.page_link("pages/5_Profile.py", label="Profile", icon="◉")
    st.title("Welcome back")
    st.write("Use the sidebar to manage your grievances and profile.")


main()