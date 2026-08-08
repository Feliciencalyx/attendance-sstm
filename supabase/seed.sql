-- ====================================================================
-- Biometric Attendance Management System - Seed Data
-- ====================================================================

-- Insert sample users with mock 128-dimensional face vectors and fingerprint templates
INSERT INTO public.users (id, employee_id, full_name, email, department, fingerprint_template, is_active)
VALUES
    ('a0000000-0000-0000-0000-000000000001', 'EMP-101', 'Sarah Connor', 'sarah.connor@example.com', 'Engineering', 'FP_TEMPLATE_BASE64_SARAH_CONNOR_9981', true),
    ('a0000000-0000-0000-0000-000000000002', 'EMP-102', 'Alex Mercer', 'alex.mercer@example.com', 'Operations', 'FP_TEMPLATE_BASE64_ALEX_MERCER_1204', true),
    ('a0000000-0000-0000-0000-000000000003', 'EMP-103', 'Elena Rostova', 'elena.rostova@example.com', 'Human Resources', 'FP_TEMPLATE_BASE64_ELENA_ROSTOVA_5512', true),
    ('a0000000-0000-0000-0000-000000000004', 'EMP-104', 'David Vance', 'david.vance@example.com', 'Finance', 'FP_TEMPLATE_BASE64_DAVID_VANCE_7743', true),
    ('a0000000-0000-0000-0000-000000000005', 'EMP-105', 'Marcus Wright', 'marcus.wright@example.com', 'Security', 'FP_TEMPLATE_BASE64_MARCUS_WRIGHT_8831', true)
ON CONFLICT (employee_id) DO NOTHING;

-- Seed attendance records for today to showcase various statuses
INSERT INTO public.attendance (user_id, date, check_in_time, status)
VALUES
    ('a0000000-0000-0000-0000-000000000001', CURRENT_DATE, (CURRENT_DATE + TIME '08:45:00'), 'PRESENT'),
    ('a0000000-0000-0000-0000-000000000002', CURRENT_DATE, (CURRENT_DATE + TIME '09:22:15'), 'LATE')
ON CONFLICT (user_id, date) DO NOTHING;
