import streamlit as st

from components.ui import format_date, page_header, status_badge
from student_common import auto_refresh, grievance_repository, notification_repository, require_authenticated_page

st.set_page_config(page_title="Dashboard | VIT Grievances", layout="wide")
require_authenticated_page()
auto_refresh(20)
page_header("Student workspace", "Your grievance overview", "A clear view of open concerns, progress, and recent updates.")
repo = grievance_repository()
try:
    grievances = repo.list_for_student()
    notifications = notification_repository().list()[:4]
except Exception:
    st.error("We could not load your dashboard. Please refresh and try again.")
    st.stop()

counts = {status: sum(item.get("status") == status for item in grievances) for status in ["submitted", "under_review", "in_progress", "resolved", "closed"]}
cols = st.columns(6)
for column, label, value in zip(cols, ["Total", "Pending", "Under Review", "In Progress", "Resolved", "Closed"], [len(grievances), counts["submitted"], counts["under_review"], counts["in_progress"], counts["resolved"], counts["closed"]]):
    with column:
        st.markdown(f'<div class="card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

st.write("")
left, right = st.columns([1.6, 1])
with left:
    st.subheader("Recent grievances")
    if not grievances: st.info("You have not submitted a grievance yet.")
    for item in grievances[:5]:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{item['title']}**")
                st.caption(f"{item.get('grievance_categories', {}).get('name', 'Category')} · {format_date(item.get('created_at'))}")
            with col2: status_badge(item["status"])
with right:
    st.subheader("Recent notifications")
    for item in notifications:
        st.markdown(f"**{item['title']}**  \n{item['message']}")
        st.caption(format_date(item.get("created_at")))
    if not notifications: st.info("No notifications yet.")