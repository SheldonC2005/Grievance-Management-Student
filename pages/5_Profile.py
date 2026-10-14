import streamlit as st

from components.ui import page_header
from student_common import auto_refresh, client, require_authenticated_page
from repositories.student_repository import StudentRepository

st.set_page_config(page_title="Profile | VIT", layout="wide")
require_authenticated_page()
auto_refresh(20)
page_header("Account", "Your profile", "Keep your contact and academic information current.")
user = st.session_state["user"]
student = StudentRepository(client()).get_by_auth_user(user.id)
if not student: st.error("Profile not found."); st.stop()
st.text_input("Student ID", value=student["student_id"], disabled=True)
with st.form("profile"):
    name = st.text_input("Name", value=student.get("name", ""))
    st.text_input("Email", value=student.get("email", ""), disabled=True, help="Email changes require a separate Supabase Auth confirmation flow.")
    phone = st.text_input("Phone", value=student.get("phone", ""))
    department = st.text_input("Department", value=student.get("department") or "")
    programme = st.text_input("Programme", value=student.get("programme") or "")
    year = st.number_input("Year", min_value=1, max_value=6, value=student.get("year") or 1)
    semester = st.number_input("Semester", min_value=1, max_value=12, value=student.get("semester") or 1)
    save = st.form_submit_button("Save profile", type="primary")
if save:
    try:
        StudentRepository(client()).update_profile(user.id, {"name": name, "phone": phone, "department": department or None, "programme": programme or None, "year": year, "semester": semester})
        st.success("Profile updated.")
        st.session_state["student"] = StudentRepository(client()).get_by_auth_user(user.id)
    except Exception: st.error("Profile could not be updated. Check the values and try again.")