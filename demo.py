from datetime import datetime

import streamlit as st


st.set_page_config(
    page_title="VIT Student Grievance Portal | Demo",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


STATUS_STYLES = {
    "Submitted": ("#2563eb", "#eff6ff", "📝"),
    "Under Review": ("#7c3aed", "#f5f3ff", "🔎"),
    "Assigned": ("#0369a1", "#e0f2fe", "👤"),
    "In Progress": ("#b45309", "#fffbeb", "⚙"),
    "Resolved": ("#15803d", "#f0fdf4", "✓"),
    "Closed": ("#475569", "#f1f5f9", "🔒"),
    "Rejected": ("#b91c1c", "#fef2f2", "!"),
    "Reopened": ("#c2410c", "#fff7ed", "↻"),
}

CATEGORIES = [
    "Academic",
    "Faculty",
    "Examination",
    "Hostel",
    "Infrastructure",
    "Transport",
    "Fees / Finance",
    "Library",
    "IT / Technical",
    "Discipline",
    "Harassment",
    "Other",
]

DEMO_STUDENT = {
    "student_id": "24BCE1234",
    "name": "Arjun Kumar",
    "email": "arjun.kumar@example.com",
    "phone": "9876543210",
    "department": "Computer Science and Engineering",
    "programme": "Integrated M.Tech",
    "year": 4,
    "semester": 7,
}

GRIEVANCES = [
    {
        "id": "GRV-2026-00121", "title": "Examination Hall Allocation Issue", "category": "Examination",
        "date": "06 Oct 2026", "updated": "08 Oct 2026", "status": "Under Review", "anonymous": False,
        "department": "Examination Cell", "description": "The examination hall assigned for the upcoming internal assessment is located far from the department and overlaps with the accessibility arrangement requested earlier.",
        "response": "Your grievance has been reviewed by the concerned department. The issue has been forwarded to the examination cell for further action.",
    },
    {
        "id": "GRV-2026-00118", "title": "Hostel Wi-Fi Connectivity", "category": "IT / Technical",
        "date": "04 Oct 2026", "updated": "07 Oct 2026", "status": "In Progress", "anonymous": False,
        "department": "Campus IT Services", "description": "The Wi-Fi connection on the third floor of the hostel drops frequently during evening study hours and affects access to academic resources.",
        "response": "The network team has scheduled an access-point inspection for the affected floor.",
    },
    {
        "id": "GRV-2026-00115", "title": "Faculty Course Registration Issue", "category": "Faculty",
        "date": "29 Sep 2026", "updated": "05 Oct 2026", "status": "Resolved", "anonymous": False,
        "department": "Academic Office", "description": "A required course was not visible in the registration portal even though the prerequisite had been completed.",
        "response": "The course visibility issue has been corrected and registration is now available.",
    },
    {
        "id": "GRV-2026-00110", "title": "Transport Bus Timing Issue", "category": "Transport",
        "date": "22 Sep 2026", "updated": "30 Sep 2026", "status": "Closed", "anonymous": False,
        "department": "Transport Office", "description": "The evening shuttle was regularly leaving before the published departure time, making it difficult to reach the hostel after laboratory sessions.",
        "response": "The published departure schedule has been reviewed with the transport team.",
    },
    {
        "id": "GRV-2026-00107", "title": "Library Access Extension Request", "category": "Library",
        "date": "18 Sep 2026", "updated": "25 Sep 2026", "status": "Resolved", "anonymous": False,
        "department": "Central Library", "description": "Request to extend weekend library access during the project submission period.",
        "response": "Weekend access was extended for the project submission period.",
    },
    {
        "id": "GRV-2026-00103", "title": "Classroom Projector Maintenance", "category": "Infrastructure",
        "date": "12 Sep 2026", "updated": "20 Sep 2026", "status": "In Progress", "anonymous": False,
        "department": "Infrastructure Services", "description": "The projector in the project classroom is displaying intermittent signal loss during presentations.",
        "response": "A replacement cable and projector inspection have been assigned.",
    },
    {
        "id": "GRV-2026-00098", "title": "Scholarship Fee Credit Clarification", "category": "Fees / Finance",
        "date": "04 Sep 2026", "updated": "09 Sep 2026", "status": "Under Review", "anonymous": True,
        "department": "Student Finance Office", "description": "Clarification requested regarding the timing of a scholarship fee credit shown in the student account.",
        "response": "The finance office is reviewing the account reconciliation details.",
    },
    {
        "id": "GRV-2026-00091", "title": "Academic Calendar Information", "category": "Academic",
        "date": "27 Aug 2026", "updated": "29 Aug 2026", "status": "Submitted", "anonymous": False,
        "department": "Academic Office", "description": "Request for clarification about the project evaluation date shown in two different academic calendar notices.",
        "response": "The request has been received and is awaiting review.",
    },
]

NOTIFICATIONS = [
    {"title": "Status updated", "message": "Your grievance GRV-2026-00121 has moved to Under Review.", "date": "08 Oct 2026", "read": False},
    {"title": "Administrator response", "message": "An administrator responded to GRV-2026-00118.", "date": "07 Oct 2026", "read": False},
    {"title": "Grievance resolved", "message": "Your grievance GRV-2026-00115 has been Resolved.", "date": "05 Oct 2026", "read": True},
    {"title": "Grievance closed", "message": "Grievance GRV-2026-00110 has been Closed.", "date": "30 Sep 2026", "read": True},
]


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root { --navy:#102a43; --ink:#243b53; --muted:#627d98; --blue:#1769aa; --paper:#f5f8fb; --line:#d9e2ec; }
        .stApp { background:var(--paper); color:var(--ink); }
        [data-testid="stSidebar"] { background:linear-gradient(180deg,#102a43 0%,#173f5f 100%); }
        [data-testid="stSidebar"] * { color:#f0f4f8; }
        [data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.16); }
        .demo-kicker { color:#1769aa; font-size:.74rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }
        .demo-title { color:#102a43; font-size:2.4rem; line-height:1.08; font-weight:800; margin:.2rem 0 .45rem; }
        .demo-subtitle { color:#627d98; font-size:1rem; margin-bottom:1.4rem; }
        .demo-banner { background:#e0f2fe; border:1px solid #7dd3fc; color:#075985; border-radius:8px; padding:.7rem 1rem; font-size:.86rem; margin-bottom:1.4rem; }
        .metric-card { background:#fff; border:1px solid #d9e2ec; border-radius:10px; padding:1rem 1.05rem; min-height:106px; box-shadow:0 5px 18px rgba(16,42,67,.05); }
        .metric-label { color:#627d98; font-size:.72rem; font-weight:800; text-transform:uppercase; letter-spacing:.06em; }
        .metric-value { color:#102a43; font-size:1.85rem; font-weight:800; margin-top:.35rem; }
        .section-title { color:#102a43; font-size:1.25rem; font-weight:800; margin:1.25rem 0 .7rem; }
        .case-card { background:#fff; border:1px solid #d9e2ec; border-radius:9px; padding:1rem 1.1rem; margin-bottom:.65rem; }
        .case-id { color:#627d98; font-size:.74rem; font-weight:700; letter-spacing:.04em; }
        .case-title { color:#102a43; font-size:1rem; font-weight:800; margin:.25rem 0; }
        .case-meta { color:#627d98; font-size:.82rem; }
        .status-badge { display:inline-block; border-radius:999px; padding:.28rem .65rem; font-size:.76rem; font-weight:800; white-space:nowrap; }
        .timeline { display:flex; align-items:flex-start; gap:0; margin:1.2rem 0; }
        .timeline-step { flex:1; text-align:center; position:relative; color:#829ab1; font-size:.75rem; font-weight:700; }
        .timeline-step:not(:last-child)::after { content:""; position:absolute; top:13px; left:58%; width:84%; height:2px; background:#d9e2ec; }
        .timeline-step.done:not(:last-child)::after { background:#93c5fd; }
        .timeline-dot { position:relative; z-index:1; margin:0 auto .45rem; width:27px; height:27px; line-height:27px; border-radius:50%; background:#e2e8f0; color:#64748b; }
        .timeline-step.done, .timeline-step.current { color:#1769aa; }
        .timeline-step.done .timeline-dot, .timeline-step.current .timeline-dot { background:#1769aa; color:#fff; }
        .profile-item { background:#fff; border-bottom:1px solid #edf2f7; padding:.75rem 0; }
        .profile-label { color:#627d98; font-size:.76rem; text-transform:uppercase; letter-spacing:.05em; }
        .profile-value { color:#102a43; font-weight:700; margin-top:.15rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def status_badge(status: str) -> str:
    color, background, icon = STATUS_STYLES[status]
    return f'<span class="status-badge" style="color:{color};background:{background}">{icon} {status}</span>'


def page_header(kicker: str, title: str, subtitle: str) -> None:
    st.markdown(f'<div class="demo-kicker">{kicker}</div><div class="demo-title">{title}</div><div class="demo-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: int) -> None:
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)


def grievance_by_id(grievance_id: str) -> dict:
    return next(item for item in GRIEVANCES if item["id"] == grievance_id)


def render_dashboard() -> None:
    page_header("Student workspace", "Your grievance overview", "Track concerns, follow responses, and stay updated on campus issues.")
    st.markdown('<div class="demo-banner"><strong>DEMO MODE</strong> — Showing fictional data. Supabase authentication and database are disabled.</div>', unsafe_allow_html=True)
    metric_values = [("Total grievances", 8), ("Pending", 2), ("Under review", 1), ("In progress", 2), ("Resolved", 2), ("Closed", 1)]
    for row_start in range(0, len(metric_values), 3):
        cols = st.columns(3)
        for column, (label, value) in zip(cols, metric_values[row_start:row_start + 3]):
            with column:
                metric_card(label, value)
        st.write("")
    left, right = st.columns([1.55, 1])
    with left:
        st.markdown('<div class="section-title">Recent grievances</div>', unsafe_allow_html=True)
        for item in GRIEVANCES[:4]:
            with st.container(border=True):
                first, second = st.columns([3, 1])
                with first:
                    st.markdown(f'<div class="case-id">{item["id"]} · {item["date"]}</div><div class="case-title">{item["title"]}</div><div class="case-meta">{item["category"]}</div>', unsafe_allow_html=True)
                with second:
                    st.markdown(status_badge(item["status"]), unsafe_allow_html=True)
    with right:
        st.markdown('<div class="section-title">Recent activity</div>', unsafe_allow_html=True)
        for item in NOTIFICATIONS[:3]:
            marker = "●" if not item["read"] else "○"
            st.markdown(f'<div class="case-card"><div class="case-title">{marker} {item["title"]}</div><div class="case-meta">{item["message"]}</div><div class="case-id">{item["date"]}</div></div>', unsafe_allow_html=True)


def render_submit() -> None:
    page_header("New request", "Submit a grievance", "Share enough detail for the concerned team to understand and act on your concern.")
    with st.form("demo_submit_form"):
        category = st.selectbox("Category", CATEGORIES)
        title = st.text_input("Title / subject", placeholder="Briefly describe the issue")
        description = st.text_area("Detailed description", height=170, placeholder="Include relevant dates, locations, and context...")
        anonymous = st.checkbox("Submit anonymously to administrators")
        files = st.file_uploader("Supporting files (optional, max 5 files)", type=["pdf", "png", "jpg", "jpeg", "doc", "docx"], accept_multiple_files=True)
        submitted = st.form_submit_button("Submit grievance", type="primary", width="stretch")
    if submitted:
        if not title.strip() or not description.strip():
            st.error("Enter a title and detailed description to continue.")
        else:
            st.success("Demo grievance submitted successfully.")
            st.info(f"Fake grievance ID: **GRV-2026-00125** · {category} · {'Anonymous' if anonymous else 'Identity visible to administrators'} · {len(files or [])} attachment(s)")


def render_grievances() -> None:
    page_header("Tracking", "My grievances", "A fictional view of grievances belonging to demo student Arjun Kumar.")
    search = st.text_input("Search grievances", placeholder="Search by title or grievance ID")
    filtered = [item for item in GRIEVANCES if not search.strip() or search.lower() in f'{item["title"]} {item["id"]}'.lower()]
    st.caption(f"{len(filtered)} grievance(s) shown")
    for item in filtered:
        with st.container(border=True):
            first, second = st.columns([4, 1])
            with first:
                st.markdown(f'<div class="case-id">{item["id"]}</div><div class="case-title">{item["title"]}</div><div class="case-meta">{item["category"]} · Submitted {item["date"]} · Updated {item["updated"]}</div>', unsafe_allow_html=True)
            with second:
                st.markdown(status_badge(item["status"]), unsafe_allow_html=True)
                if st.button("View details", key=f"details_{item['id']}", width="stretch"):
                    st.session_state["selected_grievance"] = item["id"]
    selected_id = st.session_state.get("selected_grievance")
    if selected_id:
        st.divider()
        render_details(grievance_by_id(selected_id))


def render_timeline(current_status: str) -> None:
    stages = ["Submitted", "Under Review", "Assigned", "In Progress", "Resolved", "Closed"]
    current_index = stages.index(current_status) if current_status in stages else 0
    steps = []
    for index, stage in enumerate(stages):
        state = "done" if index < current_index else "current" if index == current_index else ""
        steps.append(f'<div class="timeline-step {state}"><div class="timeline-dot">{index + 1}</div>{stage}</div>')
    st.markdown(f'<div class="timeline">{"".join(steps)}</div>', unsafe_allow_html=True)


def render_details(item: dict) -> None:
    st.markdown(f'<div class="section-title">{item["title"]}</div>', unsafe_allow_html=True)
    first, second = st.columns([2, 1])
    with first:
        st.markdown(f'<div class="case-id">{item["id"]} · {item["category"]}</div>', unsafe_allow_html=True)
        st.write(item["description"])
        st.caption(f"Submitted {item['date']} · Last updated {item['updated']}")
    with second:
        st.markdown(status_badge(item["status"]), unsafe_allow_html=True)
        st.caption("Anonymous to administrators" if item["anonymous"] else "Identity visible to administrators")
        st.caption(f"Assigned department: {item['department']}")
    st.markdown("**Status timeline**")
    render_timeline(item["status"])
    detail_left, detail_right = st.columns(2)
    with detail_left:
        st.markdown("**Admin response**")
        st.info(item["response"])
    with detail_right:
        st.markdown("**Attachments**")
        st.caption("📄 examination-allocation-details.pdf")
        st.caption("🖼️ supporting-screenshot.png")
    st.markdown("**Add information**")
    with st.form(f"reply_{item['id']}"):
        reply = st.text_area("Comment or reply", placeholder="Add a follow-up message...", label_visibility="collapsed")
        if st.form_submit_button("Send reply", width="content") and reply.strip():
            st.success("Demo reply added for this session only.")


def render_notifications() -> None:
    page_header("Updates", "Notifications", "Important updates from the fictional grievance workflow.")
    unread = sum(not item["read"] for item in NOTIFICATIONS)
    st.caption(f"{unread} unread notification(s)")
    for item in NOTIFICATIONS:
        background = "#ffffff" if item["read"] else "#eff6ff"
        border = "#d9e2ec" if item["read"] else "#93c5fd"
        marker = "Read" if item["read"] else "Unread"
        st.markdown(f'<div class="case-card" style="background:{background};border-color:{border}"><div class="case-title">{item["title"]} <span class="case-id">· {marker}</span></div><div class="case-meta">{item["message"]}</div><div class="case-id">{item["date"]}</div></div>', unsafe_allow_html=True)


def render_profile() -> None:
    page_header("Account", "Student profile", "A fictional demo profile. Changes are kept only in this browser session.")
    left, right = st.columns([1, 1.55])
    with left:
        st.markdown('<div class="metric-card"><div class="demo-kicker">VIT student</div><div class="metric-value">AK</div><div class="case-title">Arjun Kumar</div><div class="case-meta">24BCE1234</div></div>', unsafe_allow_html=True)
    with right:
        fields = [("Student ID", "student_id"), ("Name", "name"), ("Email", "email"), ("Phone", "phone"), ("Department", "department"), ("Programme", "programme"), ("Year", "year"), ("Semester", "semester")]
        for label, key in fields:
            st.markdown(f'<div class="profile-item"><div class="profile-label">{label}</div><div class="profile-value">{st.session_state.demo_profile[key]}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Edit profile</div>', unsafe_allow_html=True)
    with st.form("demo_profile_form"):
        name = st.text_input("Name", value=st.session_state.demo_profile["name"])
        phone = st.text_input("Phone", value=st.session_state.demo_profile["phone"])
        department = st.text_input("Department", value=st.session_state.demo_profile["department"])
        programme = st.text_input("Programme", value=st.session_state.demo_profile["programme"])
        save = st.form_submit_button("Save changes", type="primary", width="content")
    if save:
        st.session_state.demo_profile.update({"name": name, "phone": phone, "department": department, "programme": programme})
        st.success("Demo profile updated for this session.")


def main() -> None:
    inject_styles()
    if "demo_profile" not in st.session_state:
        st.session_state.demo_profile = DEMO_STUDENT.copy()
    with st.sidebar:
        st.markdown("## VIT Student Portal")
        st.caption("Student Grievance Management System")
        st.divider()
        page = st.radio("Navigate", ["Dashboard", "Submit Grievance", "My Grievances", "Notifications", "Profile", "Logout"], label_visibility="collapsed")
        st.divider()
        st.caption("DEMO STUDENT")
        st.markdown(f"**{st.session_state.demo_profile['name']}**")
        st.caption(st.session_state.demo_profile["student_id"])
    if page == "Dashboard":
        render_dashboard()
    elif page == "Submit Grievance":
        render_submit()
    elif page == "My Grievances":
        render_grievances()
    elif page == "Notifications":
        render_notifications()
    elif page == "Profile":
        render_profile()
    else:
        page_header("Demo session", "Logout", "This presentation build does not use authentication.")
        st.info("Demo mode — authentication is disabled.")


if __name__ == "__main__":
    st.navigation([st.Page(main, title="Student portal demo")], position="hidden").run()