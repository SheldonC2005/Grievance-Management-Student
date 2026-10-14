import time

import streamlit as st

from components.ui import inject_styles
from config.settings import get_settings
from supabase_client import authenticated_supabase, clear_demo_session, get_demo_student_record, require_demo_session, sign_in_demo_student

st.set_page_config(page_title="VIT Student Grievance Portal", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")
inject_styles()


def authenticated_demo_session() -> bool:
    try:
        require_demo_session(st.session_state)
        return True
    except RuntimeError:
        return False


def login_form() -> None:
    st.markdown(
        '<div class="portal-kicker">Vellore Institute of Technology</div><h1 class="portal-title">Student Grievance Portal</h1>',
        unsafe_allow_html=True,
    )
    st.info("Demo mode is enabled. Only the approved student accounts can sign in.")

    with st.form("demo_login"):
        student_id = st.text_input("Student ID", placeholder="24BCE1234").upper()
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", type="primary", use_container_width=True)

    if submitted:
        try:
            response = sign_in_demo_student(student_id, password)
            profile = get_demo_student_record(student_id, authenticated_supabase(response.session))
            if not profile:
                raise ValueError("The authenticated student profile was not found in the shared Supabase database.")
            st.session_state["user"] = response.user
            st.session_state["session"] = response.session
            st.session_state["student"] = profile
            st.success(f"Welcome back, {profile['name']}.")
            st.rerun()
        except ValueError as error:
            st.error(str(error))
        except Exception:
            st.error("Supabase could not complete the demo sign-in. Confirm the project URL, key, Auth user, and linked student record.")


def main() -> None:
    try:
        get_settings()
    except RuntimeError as error:
        st.error(str(error))
        st.info("Create a .env file from .env.example or configure Streamlit secrets.")
        st.stop()

    if not authenticated_demo_session():
        login_form()
        return

    student = st.session_state["student"]
    user = st.session_state["user"]
    if "last_refresh" not in st.session_state:
        st.session_state["last_refresh"] = time.monotonic()
    if time.monotonic() - st.session_state["last_refresh"] >= 20:
        st.session_state["last_refresh"] = time.monotonic()
        st.rerun()

    st.sidebar.markdown("### VIT Student Portal")
    st.sidebar.caption(f"{student['name']} · {student['student_id']}")
    if st.sidebar.button("Log out", use_container_width=True):
        try:
            from supabase_client import get_supabase

            get_supabase().auth.sign_out()
        finally:
            clear_demo_session(st.session_state)
            st.rerun()

    st.sidebar.page_link("pages/1_Dashboard.py", label="Dashboard", icon="🏠")
    st.sidebar.page_link("pages/2_Submit_Grievance.py", label="Submit grievance", icon="＋")
    st.sidebar.page_link("pages/3_My_Grievances.py", label="My grievances", icon="▣")
    st.sidebar.page_link("pages/4_Notifications.py", label="Notifications", icon="🔔")
    st.sidebar.page_link("pages/5_Profile.py", label="Profile", icon="◉")

    st.title("Welcome back")
    st.write(f"Signed in as {user.name} ({student['student_id']}).")
    st.caption("Grievance data refreshes automatically every 20 seconds.")


if __name__ == "__main__":
    main()
