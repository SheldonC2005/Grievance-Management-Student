import streamlit as st

from components.ui import format_date, page_header
from student_common import auto_refresh, notification_repository, require_authenticated_page

st.set_page_config(page_title="Notifications | VIT", layout="wide")
require_authenticated_page()
auto_refresh(20)
page_header("Updates", "Notifications", "Stay informed about responses and status changes.")
repo = notification_repository()
try: notifications = repo.list()
except Exception: st.error("Notifications could not be loaded."); st.stop()
for item in notifications:
    with st.container(border=True):
        left, right = st.columns([5, 1])
        with left:
            st.markdown(f"**{item['title']}**")
            st.write(item["message"])
            st.caption(format_date(item.get("created_at")))
        with right:
            if item.get("is_read"): st.caption("Read")
            elif st.button("Mark read", key=f"read_{item['id']}"):
                repo.mark_read(item["id"]); st.rerun()
if not notifications: st.info("You have no notifications.")