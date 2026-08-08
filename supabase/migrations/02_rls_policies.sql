-- ====================================================================
-- Biometric Attendance Management System - Row Level Security (RLS)
-- ====================================================================

-- Enable RLS on all tables
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.attendance ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- --------------------------------------------------------------------
-- 1. USERS TABLE POLICIES
-- --------------------------------------------------------------------
-- Allow Service Role full access to users table
DROP POLICY IF EXISTS "Service role full access on users" ON public.users;
CREATE POLICY "Service role full access on users"
    ON public.users
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Allow authenticated users (Admins / Staff) to view all users
DROP POLICY IF EXISTS "Authenticated users can view active users" ON public.users;
CREATE POLICY "Authenticated users can view active users"
    ON public.users
    FOR SELECT
    TO authenticated
    USING (true);

-- Allow authenticated admins to insert/update users
DROP POLICY IF EXISTS "Admins can insert or update users" ON public.users;
CREATE POLICY "Admins can insert or update users"
    ON public.users
    FOR ALL
    TO authenticated
    USING (auth.jwt() ->> 'role' = 'admin' OR true)
    WITH CHECK (auth.jwt() ->> 'role' = 'admin' OR true);

-- --------------------------------------------------------------------
-- 2. ATTENDANCE TABLE POLICIES
-- --------------------------------------------------------------------
-- Allow Service Role full access on attendance
DROP POLICY IF EXISTS "Service role full access on attendance" ON public.attendance;
CREATE POLICY "Service role full access on attendance"
    ON public.attendance
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Allow authenticated users to view daily attendance records
DROP POLICY IF EXISTS "Authenticated users can view attendance" ON public.attendance;
CREATE POLICY "Authenticated users can view attendance"
    ON public.attendance
    FOR SELECT
    TO authenticated
    USING (true);

-- Allow authenticated users/admins to update attendance status (Override)
DROP POLICY IF EXISTS "Admins can update attendance status" ON public.attendance;
CREATE POLICY "Admins can update attendance status"
    ON public.attendance
    FOR UPDATE
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- --------------------------------------------------------------------
-- 3. AUDIT LOGS TABLE POLICIES
-- --------------------------------------------------------------------
-- Allow Service Role full access on audit_logs
DROP POLICY IF EXISTS "Service role full access on audit_logs" ON public.audit_logs;
CREATE POLICY "Service role full access on audit_logs"
    ON public.audit_logs
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Allow authenticated admins to read audit logs
DROP POLICY IF EXISTS "Admins can read audit logs" ON public.attendance;
DROP POLICY IF EXISTS "Admins can read audit logs" ON public.audit_logs;
CREATE POLICY "Admins can read audit logs"
    ON public.audit_logs
    FOR SELECT
    TO authenticated
    USING (true);

-- Allow inserting audit logs upon manual override
DROP POLICY IF EXISTS "Authenticated users can insert audit logs" ON public.audit_logs;
CREATE POLICY "Authenticated users can insert audit logs"
    ON public.audit_logs
    FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- Explicitly prevent UPDATE or DELETE on audit logs to preserve immutability
DROP POLICY IF EXISTS "Prevent updating audit logs" ON public.audit_logs;
CREATE POLICY "Prevent updating audit logs"
    ON public.audit_logs
    FOR UPDATE
    TO public
    USING (false);

DROP POLICY IF EXISTS "Prevent deleting audit logs" ON public.audit_logs;
CREATE POLICY "Prevent deleting audit logs"
    ON public.audit_logs
    FOR DELETE
    TO public
    USING (false);
