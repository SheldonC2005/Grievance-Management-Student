-- Run this once against an existing project created before signup profiles
-- were moved into the database trigger.
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
        )
        on conflict (auth_user_id) do nothing;
    end if;
    return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
    after insert on auth.users
    for each row execute function public.handle_new_student();