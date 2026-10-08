insert into public.grievance_categories (name, description) values
('Academic', 'Curriculum, course, or academic process concerns'),
('Faculty', 'Faculty interaction or teaching concerns'),
('Examination', 'Examination, evaluation, or results concerns'),
('Hostel', 'Hostel facilities or accommodation concerns'),
('Infrastructure', 'Campus buildings, facilities, or maintenance concerns'),
('Transport', 'Campus transport and mobility concerns'),
('Fees / Finance', 'Fees, payments, scholarships, or finance concerns'),
('Library', 'Library access, resources, or services concerns'),
('IT / Technical', 'Technical systems, network, or portal concerns'),
('Discipline', 'Disciplinary process or conduct concerns'),
('Harassment', 'Harassment or safety concerns'),
('Other', 'Other student concerns')
on conflict (name) do update set description = excluded.description, is_active = true;