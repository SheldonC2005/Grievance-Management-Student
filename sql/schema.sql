create extension if not exists "pgcrypto";

create type public.grievance_status as enum ('submitted', 'under_review', 'assigned', 'in_progress', 'resolved', 'closed', 'rejected', 'reopened');
create type public.comment_author_role as enum ('student', 'admin');

create table public.students (
    auth_user_id uuid primary key references auth.users(id) on delete cascade,
    student_id text not null unique check (student_id ~ '^[0-9]{2}[A-Z]{3}[0-9]{4}$'),
    name text not null check (length(trim(name)) between 2 and 120),
    email text not null unique,
    phone text not null check (length(trim(phone)) between 7 and 20),
    department text,
    programme text,
    year smallint check (year is null or year between 1 and 6),
    semester smallint check (semester is null or semester between 1 and 12),
    created_at timestamptz not null default timezone('utc', now()),
    updated_at timestamptz not null default timezone('utc', now())
);

create or replace function public.handle_new_student() returns trigger
language plpgsql security definer set search_path = public as $$
begin
    if new.raw_user_meta_data ? 'student_id' then
        insert into public.students (auth_user_id, student_id, name, email, phone)
        values (
            new.id,
            upper(trim(new.raw_user_meta_data ->> 'student_id')),
            trim(new.raw_user_meta_data ->> 'name'),
            lower(trim(new.email)),
            trim(new.raw_user_meta_data ->> 'phone')
        );
    end if;
    return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
    after insert on auth.users
    for each row execute function public.handle_new_student();

create table public.grievance_categories (
    id uuid primary key default gen_random_uuid(),
    name text not null unique,
    description text,
    is_active boolean not null default true,
    created_at timestamptz not null default timezone('utc', now())
);

create table public.grievances (
    id uuid primary key default gen_random_uuid(),
    student_auth_user_id uuid not null references public.students(auth_user_id) on delete cascade,
    category_id uuid not null references public.grievance_categories(id),
    title text not null check (length(trim(title)) between 3 and 160),
    description text not null check (length(trim(description)) between 20 and 10000),
    is_anonymous boolean not null default false,
    status public.grievance_status not null default 'submitted',
    created_at timestamptz not null default timezone('utc', now()),
    updated_at timestamptz not null default timezone('utc', now()),
    resolved_at timestamptz,
    closed_at timestamptz
);

create table public.grievance_status_history (
    id uuid primary key default gen_random_uuid(),
    grievance_id uuid not null references public.grievances(id) on delete cascade,
    old_status public.grievance_status,
    new_status public.grievance_status not null,
    changed_by uuid references auth.users(id) on delete set null,
    changed_at timestamptz not null default timezone('utc', now()),
    remarks text
);

create table public.grievance_comments (
    id uuid primary key default gen_random_uuid(),
    grievance_id uuid not null references public.grievances(id) on delete cascade,
    author_user_id uuid not null references auth.users(id) on delete cascade,
    author_role public.comment_author_role not null,
    comment text not null check (length(trim(comment)) between 1 and 5000),
    created_at timestamptz not null default timezone('utc', now())
);

create table public.grievance_attachments (
    id uuid primary key default gen_random_uuid(),
    grievance_id uuid not null references public.grievances(id) on delete cascade,
    file_name text not null,
    storage_path text not null unique,
    file_type text not null,
    file_size integer not null check (file_size > 0 and file_size <= 10485760),
    uploaded_by uuid not null references auth.users(id) on delete cascade,
    created_at timestamptz not null default timezone('utc', now())
);

create table public.notifications (
    id uuid primary key default gen_random_uuid(),
    student_auth_user_id uuid not null references public.students(auth_user_id) on delete cascade,
    grievance_id uuid references public.grievances(id) on delete cascade,
    title text not null,
    message text not null,
    is_read boolean not null default false,
    created_at timestamptz not null default timezone('utc', now())
);

create index grievances_student_idx on public.grievances(student_auth_user_id, created_at desc);
create index grievances_status_idx on public.grievances(status);
create index grievances_category_idx on public.grievances(category_id);
create index history_grievance_idx on public.grievance_status_history(grievance_id, changed_at);
create index comments_grievance_idx on public.grievance_comments(grievance_id, created_at);
create index notifications_student_idx on public.notifications(student_auth_user_id, created_at desc);

create or replace function public.set_updated_at() returns trigger language plpgsql as $$
begin new.updated_at = timezone('utc', now()); return new; end;
$$;
create trigger students_updated_at before update on public.students for each row execute function public.set_updated_at();
create trigger grievances_updated_at before update on public.grievances for each row execute function public.set_updated_at();

create or replace function public.protect_student_identity() returns trigger language plpgsql as $$
begin
    if new.auth_user_id <> old.auth_user_id or new.student_id <> old.student_id or new.email <> old.email then
        raise exception 'Authentication identity, Student ID, and email are immutable';
    end if;
    return new;
end;
$$;
create trigger students_identity_guard before update on public.students for each row execute function public.protect_student_identity();

create or replace function public.protect_notification_fields() returns trigger language plpgsql as $$
begin
    if new.student_auth_user_id <> old.student_auth_user_id or new.grievance_id is distinct from old.grievance_id or new.title <> old.title or new.message <> old.message then
        raise exception 'Notification content and ownership are immutable';
    end if;
    return new;
end;
$$;
create trigger notifications_fields_guard before update on public.notifications for each row execute function public.protect_notification_fields();

create or replace function public.resolve_student_email(p_student_id text) returns text language sql security definer set search_path = public as $$
    select email from public.students where student_id = upper(trim(p_student_id)) limit 1;
$$;
revoke all on function public.resolve_student_email(text) from public;
grant execute on function public.resolve_student_email(text) to anon, authenticated;

insert into storage.buckets (id, name, public) values ('grievance-attachments', 'grievance-attachments', false) on conflict (id) do nothing;