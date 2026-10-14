import logging

import streamlit as st

from components.ui import page_header
from student_common import auto_refresh, client, current_user_id, grievance_repository, require_authenticated_page
from services.grievance_service import GrievanceService

st.set_page_config(page_title="Submit Grievance | VIT", layout="wide")
require_authenticated_page()
auto_refresh(20)
page_header("New request", "Submit a grievance", "Give the concerned team enough detail to understand and act on your concern.")
repo = grievance_repository()
try: categories = repo.categories()
except Exception: st.error("Categories could not be loaded."); st.stop()
if not categories: st.warning("No active categories are configured yet."); st.stop()

st.caption("Attachment uploads are disabled in this demonstration.")
with st.form("grievance_form"):
    category = st.selectbox("Category", categories, format_func=lambda item: item["name"])
    title = st.text_input("Title / subject", max_chars=160)
    description = st.text_area("Detailed description", height=220, max_chars=10000)
    anonymous = st.checkbox("Submit anonymously to administrators")
    submit = st.form_submit_button("Submit grievance", type="primary")
if submit:
    try:
        grievance = GrievanceService(client(), "grievance-attachments").submit(current_user_id(), category["id"], title, description, anonymous, [])
        st.success(f"Grievance submitted successfully. ID: {grievance['id']}")
        st.page_link("pages/3_My_Grievances.py", label="View my grievances")
    except Exception as error:
        logging.getLogger(__name__).exception("Grievance submission failed")
        st.error(str(error) if isinstance(error, ValueError) else "Submission failed. Please try again.")