-- ====================================================================
-- Biometric Attendance Management System - Database Schema Migration
-- ====================================================================

-- 1. Enable pgvector extension for biometric face embedding storage
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Create Attendance Status Enum Type
DO $$ BEGIN
    CREATE TYPE attendance_status_enum AS ENUM ('PRESENT', 'ABSENT', 'EXCUSED', 'LATE');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 3. Users Table
-- Stores user profiles, biometric face vectors (128-d arrays), and fingerprint templates
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    department VARCHAR(100) DEFAULT 'General',
    face_embedding vector(128), -- 128-dimensional facial embedding vector
    fingerprint_template TEXT,  -- Base64 encoded fingerprint template
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Attendance Table
-- Daily attendance records per user
CREATE TABLE IF NOT EXISTS public.attendance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    check_in_time TIMESTAMPTZ,
    status attendance_status_enum NOT NULL DEFAULT 'PRESENT',
    override_reason TEXT,
    modified_by UUID REFERENCES public.users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT unique_user_daily_attendance UNIQUE (user_id, date)
);

-- 5. Audit Logs Table
-- Audit trail tracking manual status overrides by admins
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attendance_id UUID NOT NULL REFERENCES public.attendance(id) ON DELETE CASCADE,
    action VARCHAR(50) NOT NULL DEFAULT 'STATUS_OVERRIDE',
    previous_status attendance_status_enum,
    new_status attendance_status_enum NOT NULL,
    reason TEXT NOT NULL,
    performed_by UUID REFERENCES public.users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Indexes for High-Performance Queries
CREATE INDEX IF NOT EXISTS idx_attendance_user_date ON public.attendance(user_id, date);
CREATE INDEX IF NOT EXISTS idx_attendance_date ON public.attendance(date);
CREATE INDEX IF NOT EXISTS idx_users_employee_id ON public.users(employee_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_attendance_id ON public.audit_logs(attendance_id);

-- HNSW Vector Index for Cosine Similarity Face Matching
CREATE INDEX IF NOT EXISTS idx_users_face_embedding ON public.users 
USING hnsw (face_embedding vector_cosine_ops);

-- 7. Automatic Updated-At Trigger Function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_users_updated_at ON public.users;
CREATE TRIGGER set_users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS set_attendance_updated_at ON public.attendance;
CREATE TRIGGER set_attendance_updated_at
    BEFORE UPDATE ON public.attendance
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 8. Stored RPC Function for Vector Cosine Similarity Search
-- Calculates 1 - (face_embedding <=> query_embedding) which is cosine similarity
CREATE OR REPLACE FUNCTION match_face_embeddings(
    query_embedding vector(128),
    match_threshold FLOAT DEFAULT 0.80,
    match_count INT DEFAULT 1
)
RETURNS TABLE (
    id UUID,
    employee_id VARCHAR,
    full_name VARCHAR,
    email VARCHAR,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id,
        u.employee_id,
        u.full_name,
        u.email,
        (1 - (u.face_embedding <=> query_embedding))::FLOAT AS similarity
    FROM public.users u
    WHERE u.is_active = TRUE
      AND u.face_embedding IS NOT NULL
      AND (1 - (u.face_embedding <=> query_embedding)) >= match_threshold
    ORDER BY similarity DESC
    LIMIT match_count;
END;
$$;
