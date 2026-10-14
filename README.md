# VIT Student Grievance Management System - Student Portal

This repository contains the student-facing Streamlit portal. It connects to the shared Supabase project used by the student and admin portals. The current login is a controlled demonstration flow, not production authentication.

## Features

- Approved demo login and Supabase Auth-backed logout
- Student dashboard with automatic refresh about every 20 seconds
- Live grievance categories, submission, search, filtering, details, status history, and admin responses
- Notifications with unread state and mark-as-read support
- Student profile viewing and editing
- Anonymous-to-administrators display option while retaining the authenticated ownership link
- Attachments intentionally disabled in the demonstration UI and rejected by the service

## Project structure

- `student_app.py`: only Streamlit entry point; start this file
- `supabase_client.py`: configuration, Supabase client caching, Auth session binding, and demo-account validation
- `student_common.py`: authenticated page guard, session-aware client access, and shared refresh/repository helpers
- `pages/`: student dashboard, submission, tracking, notifications, profile, and detail pages
- `components/`, `config/`, `repositories/`, `services/`, `models/`, `utils/`: reusable application layers
- `sql/`: schema, policy reference, seed data, and the historical signup-trigger script
- `tests/`: offline unit tests using mocks where appropriate

## Requirements and setup

Use Python 3.11 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `SUPABASE_URL` to the shared project URL and `SUPABASE_KEY` to its publishable/anon key in the local `.env`. `APP_URL` may remain `http://localhost:8501`. Streamlit deployments may provide the same values through `.streamlit/secrets.toml`; never use or commit a service-role key.

Start the portal with:

```powershell
.\.venv\Scripts\python.exe -m streamlit run student_app.py
```

To demonstrate from two laptops, install the same dependencies on both, configure both with the same Supabase URL and publishable/anon key, and start each local portal. The shared project must already contain the Auth users and matching `public.students` rows:

`auth.users.id` -> `students.auth_user_id`, with unique `student_id` and matching `email`.

The approved demonstration credentials are:

- `24BCE1234` / `abcd123`
- `24BCE5678` / `abcd123`

These credentials are for demonstration only. The app resolves the email through the existing `resolve_student_email` RPC, signs in through Supabase Auth, binds the returned access/refresh token pair to the cached client, and then resolves the profile by the authenticated Auth UUID. It does not fabricate UUIDs or accept a Student ID as proof of ownership.

## Database contract

The application uses the actual table name `public.grievances`, not `greivances`. Other required tables are `students`, `grievance_categories`, `grievance_status_history`, `grievance_comments`, `grievance_attachments`, and `notifications`. Categories and records are read from Supabase; the app does not create fake live data during startup or verification.

The SQL files describe the intended relationships and RLS policies. No migration is run by this application. The existing attachment table and storage bucket are preserved, but uploads are disabled for this demonstration.

## Current RLS warning

Per the current Supabase dashboard configuration, RLS is disabled for `grievance_attachments`, `grievance_categories`, `grievance_comments`, `grievance_status_history`, `grievances`, `notifications`, and `students`. The local `sql/policies.sql` file is retained as the intended policy reference, but those policies cannot protect the live tables while RLS is disabled.

The approved-account allowlist and application checks reduce accidental misuse in this controlled demo, but they are not equivalent to database-enforced student isolation. Do not treat this deployment as production-secure or expose it publicly until an appropriate RLS authorization model is restored and tested.

## Testing and verification

The automated suite is offline and uses mocks for Supabase behavior where needed; passing it does not prove live connectivity or live authorization.

```powershell
python -m pytest -q
python -m compileall student_app.py config components models repositories services utils pages
```

Live integration was not claimed unless a configured Supabase project was reachable and tested without creating, modifying, or deleting real data. Before relying on a deployment, verify the project URL/key, Auth users, student links, RPC permissions, actual table names, and the live RLS state in the Supabase dashboard.

## Cleanup record

- Deleted `app.py`: older signup-capable entry point with a separate authentication path; no remaining imports or startup references after `student_app.py` was confirmed as primary.
- Deleted `demo.py`: fictional in-memory prototype that bypassed Supabase and displayed fake records; no remaining imports or references.
- Deleted `services/supabase_client.py`: duplicate one-function wrapper; all callers use the root `supabase_client.py` directly.

Retained `services/auth_service.py` because it is a reusable service for the existing Auth/signup architecture, although the controlled student entry point intentionally does not expose public signup. Retained all SQL, attachment, repository, page, test, environment-template, and configuration files required by the current portal or deployment contract.
