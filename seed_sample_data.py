import sys
from supabase_client import get_supabase

sys.stdout.reconfigure(encoding="utf-8")

db = get_supabase()
auth_res = db.auth.sign_in_with_password({"email": "demo1@student.com", "password": "abcd123"})
client = db
client.auth.set_session(auth_res.session.access_token, auth_res.session.refresh_token)

user_a_id = "d9917f66-c727-442d-938d-0c859eb0a2b5" # 24BCE1234
user_b_id = "6ebf2194-dc03-4147-8f78-91f7fa599cf7" # 24BCE5678

# Map categories
categories = client.table("grievance_categories").select("id, name").execute().data
cat_map = {c["name"]: c["id"] for c in categories}

# Check existing grievances
existing = client.table("grievances").select("id").execute().data
if existing:
    print(f"Already found {len(existing)} grievances. Deleting them to reseed clean consistent demo data...")
    for item in existing:
        client.table("grievances").delete().eq("id", item["id"]).execute()

print("Inserting grievances for Demo Student A (24BCE1234)...")
grievances_data = [
    {
        "student_auth_user_id": user_a_id,
        "category_id": cat_map["Hostel"],
        "title": "Air Conditioner malfunctioning in Room D-408",
        "description": "The AC unit in block D room 408 has been leaking water and not cooling since Monday. We submitted a hostel warden note but it requires maintenance team inspection.",
        "is_anonymous": False,
        "status": "in_progress",
    },
    {
        "student_auth_user_id": user_a_id,
        "category_id": cat_map["Academic"],
        "title": "Course credit clash between elective and core lab",
        "description": "The slot for Advanced Machine Learning (CSE4001) is clashing with the scheduled Distributed Systems laboratory on Wednesday afternoon.",
        "is_anonymous": False,
        "status": "under_review",
    },
    {
        "student_auth_user_id": user_a_id,
        "category_id": cat_map["IT / Technical"],
        "title": "V-TOP portal timeout during exam timetable download",
        "description": "Whenever downloading the official end-semester PDF timetable on the campus WiFi network, V-TOP drops connection and shows 504 Gateway Timeout error.",
        "is_anonymous": True,
        "status": "resolved",
    },
    {
        "student_auth_user_id": user_a_id,
        "category_id": cat_map["Library"],
        "title": "Access to IEEE Xplore digital library subscription issue",
        "description": "Unable to download full-text IEEE conference proceedings from the campus proxy. Access says subscription credentials expired for department IP range.",
        "is_anonymous": False,
        "status": "submitted",
    },
    {
        "student_auth_user_id": user_a_id,
        "category_id": cat_map["Infrastructure"],
        "title": "Water dispenser filter replacement in SJT 3rd Floor",
        "description": "The drinking water cooler and dispenser near SJT Room 315 displays a red replace-filter light indicator and water flow has become very slow.",
        "is_anonymous": False,
        "status": "closed",
    },
    {
        "student_auth_user_id": user_b_id,
        "category_id": cat_map["Transport"],
        "title": "Late evening campus shuttle bus frequency",
        "description": "The shuttle bus frequency between Men's Hostel Block and Main Gate after 8:30 PM is insufficient leading to overcrowded buses.",
        "is_anonymous": False,
        "status": "under_review",
    }
]

created_grievances = []
for g in grievances_data:
    res = client.table("grievances").insert(g).execute()
    created_grievances.append(res.data[0])

print(f"Created {len(created_grievances)} grievances.")

g_ac = created_grievances[0] # in_progress
g_clash = created_grievances[1] # under_review
g_vtop = created_grievances[2] # resolved
g_lib = created_grievances[3] # submitted
g_water = created_grievances[4] # closed

print("Inserting status timeline history...")
history_records = [
    # g_ac
    {"grievance_id": g_ac["id"], "old_status": None, "new_status": "submitted", "remarks": "Grievance submitted by student."},
    {"grievance_id": g_ac["id"], "old_status": "submitted", "new_status": "under_review", "remarks": "Assigned to Hostel Maintenance Division."},
    {"grievance_id": g_ac["id"], "old_status": "under_review", "new_status": "in_progress", "remarks": "Technician dispatched to Room D-408 with replacement coil."},
    # g_clash
    {"grievance_id": g_clash["id"], "old_status": None, "new_status": "submitted", "remarks": "Grievance submitted by student."},
    {"grievance_id": g_clash["id"], "old_status": "submitted", "new_status": "under_review", "remarks": "Forwarded to Academic Scheduling Deanery."},
    # g_vtop
    {"grievance_id": g_vtop["id"], "old_status": None, "new_status": "submitted", "remarks": "Grievance submitted anonymously."},
    {"grievance_id": g_vtop["id"], "old_status": "submitted", "new_status": "under_review", "remarks": "IT infrastructure team alerted."},
    {"grievance_id": g_vtop["id"], "old_status": "under_review", "new_status": "resolved", "remarks": "Server load balancing reconfigured and gateway timeout limit increased."},
    # g_lib
    {"grievance_id": g_lib["id"], "old_status": None, "new_status": "submitted", "remarks": "Submitted and queued for Central Library Review."},
    # g_water
    {"grievance_id": g_water["id"], "old_status": None, "new_status": "submitted", "remarks": "Initial report received."},
    {"grievance_id": g_water["id"], "old_status": "submitted", "new_status": "resolved", "remarks": "Filter cartridge replaced and TDS level verified at 85 ppm."},
    {"grievance_id": g_water["id"], "old_status": "resolved", "new_status": "closed", "remarks": "Ticket verified by estate officer and closed."},
]
for h in history_records:
    client.table("grievance_status_history").insert(h).execute()

print("Inserting admin and student comments...")
comment_records = [
    {
        "grievance_id": g_ac["id"],
        "author_user_id": user_a_id,
        "author_role": "admin",
        "comment": "Maintenance technician Mr. Ramesh will visit Block D tomorrow between 10:00 AM and 12:00 PM. Please ensure one room resident is available.",
    },
    {
        "grievance_id": g_clash["id"],
        "author_user_id": user_a_id,
        "author_role": "admin",
        "comment": "The scheduling committee is reviewing the slot matrix for winter semester. A slot reallocation notice will be posted by Friday.",
    },
    {
        "grievance_id": g_vtop["id"],
        "author_user_id": user_a_id,
        "author_role": "admin",
        "comment": "The gateway timeout was addressed by increasing Nginx upstream limits. Please clear browser cache and retry.",
    },
    {
        "grievance_id": g_water["id"],
        "author_user_id": user_a_id,
        "author_role": "admin",
        "comment": "Sanitation maintenance team has fitted a new filter cartridge and sanitized the reservoir.",
    }
]
for c in comment_records:
    client.table("grievance_comments").insert(c).execute()

print("Inserting notifications...")
# Clear existing notifications
client.table("notifications").delete().eq("student_auth_user_id", user_a_id).execute()

notification_records = [
    {
        "student_auth_user_id": user_a_id,
        "grievance_id": g_ac["id"],
        "title": "Maintenance Update: AC Issue in Room D-408",
        "message": "Your grievance status was updated to In Progress. Technician assigned for 10:00 AM inspection tomorrow.",
        "is_read": False,
    },
    {
        "student_auth_user_id": user_a_id,
        "grievance_id": g_clash["id"],
        "title": "Review Underway: Course Credit Clash",
        "message": "Academic Scheduling office has reviewed your course clash report. Status changed to Under Review.",
        "is_read": False,
    },
    {
        "student_auth_user_id": user_a_id,
        "grievance_id": g_vtop["id"],
        "title": "Resolved: V-TOP Portal Timeout",
        "message": "IT team has marked your grievance as Resolved. Please review and verify the fix.",
        "is_read": True,
    },
    {
        "student_auth_user_id": user_a_id,
        "grievance_id": g_water["id"],
        "title": "Closed: Water Dispenser Filter SJT",
        "message": "Maintenance completed and water filter replacement verified. Grievance closed.",
        "is_read": True,
    },
]
for n in notification_records:
    client.table("notifications").insert(n).execute()

print("Database population complete and consistent!")
