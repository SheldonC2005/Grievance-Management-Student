alter table public.students enable row level security;
alter table public.grievance_categories enable row level security;
alter table public.grievances enable row level security;
alter table public.grievance_status_history enable row level security;
alter table public.grievance_comments enable row level security;
alter table public.grievance_attachments enable row level security;
alter table public.notifications enable row level security;

create policy students_select_own on public.students for select using (auth_user_id = auth.uid());
create policy students_insert_self on public.students for insert with check (auth_user_id = auth.uid());
create policy students_update_allowed on public.students for update using (auth_user_id = auth.uid()) with check (auth_user_id = auth.uid());

create policy categories_select_active on public.grievance_categories for select to authenticated using (is_active = true);
create policy grievances_select_own on public.grievances for select using (student_auth_user_id = auth.uid());
create policy grievances_insert_own on public.grievances for insert with check (student_auth_user_id = auth.uid() and exists (select 1 from public.grievance_categories c where c.id = category_id and c.is_active = true));
create policy history_select_own on public.grievance_status_history for select using (exists (select 1 from public.grievances g where g.id = grievance_id and g.student_auth_user_id = auth.uid()));
create policy history_insert_initial_own on public.grievance_status_history for insert with check (new_status = 'submitted' and old_status is null and changed_by = auth.uid() and exists (select 1 from public.grievances g where g.id = grievance_id and g.student_auth_user_id = auth.uid() and g.status = 'submitted'));
create policy comments_select_own on public.grievance_comments for select using (exists (select 1 from public.grievances g where g.id = grievance_id and g.student_auth_user_id = auth.uid()));
create policy comments_insert_student_own on public.grievance_comments for insert with check (author_user_id = auth.uid() and author_role = 'student' and exists (select 1 from public.grievances g where g.id = grievance_id and g.student_auth_user_id = auth.uid()));
create policy attachments_select_own on public.grievance_attachments for select using (exists (select 1 from public.grievances g where g.id = grievance_id and g.student_auth_user_id = auth.uid()));
create policy attachments_insert_own on public.grievance_attachments for insert with check (uploaded_by = auth.uid() and exists (select 1 from public.grievances g where g.id = grievance_id and g.student_auth_user_id = auth.uid()));
create policy notifications_select_own on public.notifications for select using (student_auth_user_id = auth.uid());
create policy notifications_update_read on public.notifications for update using (student_auth_user_id = auth.uid()) with check (student_auth_user_id = auth.uid());

create policy storage_select_own on storage.objects for select to authenticated using (bucket_id = 'grievance-attachments' and (storage.foldername(name))[1] in (select g.id::text from public.grievances g where g.student_auth_user_id = auth.uid()));
create policy storage_insert_own on storage.objects for insert to authenticated with check (bucket_id = 'grievance-attachments' and (storage.foldername(name))[1] in (select g.id::text from public.grievances g where g.student_auth_user_id = auth.uid()));
create policy storage_delete_own on storage.objects for delete to authenticated using (bucket_id = 'grievance-attachments' and owner_id = auth.uid()::text);