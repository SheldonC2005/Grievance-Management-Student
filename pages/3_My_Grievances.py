import streamlit as st

from components.ui import format_date, page_header, status_badge
from pages.common import grievance_repository

st.set_page_config(page_title="My Grievances | VIT", layout="wide")
page_header("Tracking", "My grievances", "Only grievances belonging to your authenticated student account are returned by the database.")
repo = grievance_repository()
try: categories = repo.categories()
except Exception: categories = []
col1, col2, col3 = st.columns([2, 1, 1])
with col1: search = st.text_input("Search by title")
with col2: status = st.selectbox("Status", ["All", "submitted", "under_review", "assigned", "in_progress", "resolved", "closed", "rejected", "reopened"])
with col3: category = st.selectbox("Category", [{"id": "", "name": "All"}] + categories, format_func=lambda item: item["name"])
try: grievances = repo.list_for_student(search, None if status == "All" else status, category["id"] or None)
except Exception: st.error("Grievances could not be loaded."); st.stop()
st.caption(f"{len(grievances)} grievance(s)")
for item in grievances:
    with st.container(border=True):
        left, right = st.columns([4, 1])
        with left:
            st.markdown(f"**{item['title']}**")
            st.caption(f"{item.get('grievance_categories', {}).get('name', 'Category')} · Submitted {format_date(item.get('created_at'))} · Updated {format_date(item.get('updated_at'))}")
            st.caption(f"ID: {item['id']} {'· Anonymous' if item.get('is_anonymous') else ''}")
        with right:
            status_badge(item["status"])
            if st.button("Open", key=f"open_{item['id']}"):
                st.session_state["selected_grievance"] = item["id"]
                st.switch_page("pages/6_Grievance_Details.py")