import streamlit as st

from components.ui import format_date, page_header, status_badge
from student_common import auto_refresh, grievance_repository, require_authenticated_page

st.set_page_config(page_title="Grievance Details | VIT", layout="wide")
require_authenticated_page()
auto_refresh(20)
grievance_id = st.session_state.get("selected_grievance")
if not grievance_id: st.warning("Select a grievance from My Grievances."); st.stop()
repo = grievance_repository()
try:
    grievance = repo.get(grievance_id)
    history, comments, attachments = repo.history(grievance_id), repo.comments(grievance_id), repo.attachments(grievance_id)
except Exception: st.error("Details could not be loaded."); st.stop()
if not grievance: st.error("Grievance not found."); st.stop()
page_header("Case details", grievance["title"], f"Grievance ID: {grievance['id']}")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("### Description")
    st.write(grievance["description"])
    st.caption(f"Submitted {format_date(grievance.get('created_at'))} · Last updated {format_date(grievance.get('updated_at'))}")
with col2:
    st.markdown("### Current status")
    status_badge(grievance["status"])
    st.caption("Anonymous to administrators" if grievance.get("is_anonymous") else "Identity visible to administrators")
st.divider()
st.subheader("Status timeline")
for item in history:
    st.markdown(f"**{item['new_status'].replace('_', ' ').title()}** · {format_date(item.get('changed_at'))}")
    if item.get("remarks"): st.caption(item["remarks"])
st.subheader("Admin responses")
admin_comments = [item for item in comments if item.get("author_role") == "admin"]
if not admin_comments: st.info("No admin response has been added yet.")
for item in admin_comments:
    with st.container(border=True): st.write(item["comment"]); st.caption(format_date(item.get("created_at")))
st.subheader("Attachments")
if not attachments: st.caption("No attachments.")
for item in attachments:
    try:
        url = __import__("services.attachment_service", fromlist=["AttachmentService"]).AttachmentService(__import__("pages.common", fromlist=["client"]).client(), "grievance-attachments").signed_url(item["storage_path"])
        st.link_button(item["file_name"], url)
    except Exception: st.caption(item["file_name"])