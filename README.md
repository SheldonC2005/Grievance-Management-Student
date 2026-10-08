# VIT Student Grievance Management System - Student Portal

Student-facing Streamlit application for Vellore Institute of Technology's Student Grievance Management System. It uses Supabase Authentication, PostgreSQL, Row Level Security, and Storage. The database is a shared contract intended for a future admin portal repository.

## Architecture

```text
Streamlit UI -> Python services -> repositories -> Supabase Python client
									  |-> Auth
									  |-> PostgreSQL / RLS
									  `-> Storage
```

## Features

- Student ID/password signup and login through Supabase Auth
- Secure student-only grievance access enforced by PostgreSQL RLS
- Categorised, optionally anonymous grievances with status timeline
- Attachment validation and Supabase Storage metadata
- Admin responses, in-app notifications, searching, filtering, and profile editing

## Project structure

- `app.py`: authentication gate and application shell
- `pages/`: Streamlit pages for dashboard, submission, tracking, notifications, and profile
- `components/`: reusable presentation helpers
- `config/`, `repositories/`, `services/`, `models/`, `utils/`: application layers
- `sql/`: shared Supabase schema, RLS policies, and category seed data
- `tests/`: offline unit tests

## Setup

1. Create a Supabase project and enable Email provider authentication.
2. Run `sql/schema.sql`, then `sql/policies.sql`, then `sql/seed.sql` in the Supabase SQL editor. If the project was already created from an earlier version, run `sql/001_signup_profile_trigger.sql` once as well.
3. Install dependencies: `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and provide the publishable/anon key.
5. Run `streamlit run app.py`.

The storage bucket is created by `schema.sql`. Supabase Auth email confirmation may be disabled for local development, or students must confirm their email before first login.

## Environment configuration

```text
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-publishable-or-anon-key
APP_URL=http://localhost:8501
```

Never put a service-role key in this repository, Streamlit secrets, or the browser-facing app. Streamlit Community Cloud can use the same names in its Secrets configuration.

In Supabase Dashboard > Authentication > URL Configuration, add `http://localhost:8501` to Redirect URLs for local development. The app passes `APP_URL` as the email confirmation redirect. For deployment, set `APP_URL` to the deployed Streamlit URL and add that URL to the same Redirect URLs list.

## SQL execution order

Run `sql/schema.sql`, `sql/policies.sql`, and `sql/seed.sql` in that order. `schema.sql` creates tables, enums, helper functions, indexes, the Storage bucket, and the signup profile trigger. `policies.sql` enables RLS and adds student policies. `seed.sql` inserts the initial active categories. Existing deployments should run `sql/001_signup_profile_trigger.sql` once before using signup.

## Shared Supabase Database Contract

`auth.users.id` has a one-to-one relationship with `students.auth_user_id`. A student owns many `grievances`; each grievance references one `grievance_categories` row and owns status history, comments, attachment metadata, and notifications. The student relationship is retained when `grievances.is_anonymous` is true: anonymity is an administrator UI display rule, not database deletion of identity.

The controlled status values are `submitted`, `under_review`, `assigned`, `in_progress`, `resolved`, `closed`, `rejected`, and `reopened`. Status transitions are administrator-owned and every change is preserved in `grievance_status_history`. Categories are data in `grievance_categories`, not Python constants. Attachments use the `grievance-attachments` Storage bucket and paths `<grievance UUID>/<generated UUID>.<extension>`; PostgreSQL stores metadata only. Notifications belong to a student and optionally reference a grievance.

Student RLS policies derive ownership from `auth.uid()` through `students.auth_user_id`. Students can read their own records, create only their own grievances/comments/attachments, update only permitted profile and notification fields, and cannot write statuses, history, or admin comments. The future admin portal must use an explicitly designed admin authorization model and must respect `is_anonymous` when displaying identity.

## Deployment

Deploy `app.py` to Streamlit Community Cloud, set `SUPABASE_URL` and `SUPABASE_KEY` in App Settings > Secrets, and keep SQL migrations applied to the shared Supabase project. Do not deploy with a service-role key.

## Development checks

```bash
python -m pytest
python -m compileall app.py config components models repositories services utils pages
```