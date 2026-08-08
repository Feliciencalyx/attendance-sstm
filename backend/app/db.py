import logging
from typing import Optional, Dict, Any, List
from supabase import create_client, Client
from app.config import settings

logger = logging.getLogger("attendance.db")

supabase: Optional[Client] = None

try:
    if settings.SUPABASE_URL and "placeholder" not in settings.SUPABASE_URL:
        key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_KEY
        supabase = create_client(settings.SUPABASE_URL, key)
        logger.info("Successfully connected to Supabase client.")
    else:
        logger.warning("Supabase URL not configured or set to placeholder. Operating in Standalone In-Memory Mode.")
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {e}. Falling back to Standalone In-Memory Mode.")
    supabase = None


class MockDatabaseStore:
    """
    In-memory data store replicating PostgreSQL Supabase structure for local testing & instant demonstration.
    """
    def __init__(self):
        self.users: List[Dict[str, Any]] = [
            {
                "id": "a0000000-0000-0000-0000-000000000001",
                "employee_id": "EMP-101",
                "full_name": "Sarah Connor",
                "email": "sarah.connor@example.com",
                "department": "Engineering",
                "face_embedding": [0.05 * (i % 5) for i in range(128)],
                "fingerprint_template": "FP_TEMPLATE_SARAH_CONNOR_9981",
                "is_active": True,
                "created_at": "2026-08-01T08:00:00Z"
            },
            {
                "id": "a0000000-0000-0000-0000-000000000002",
                "employee_id": "EMP-102",
                "full_name": "Alex Mercer",
                "email": "alex.mercer@example.com",
                "department": "Operations",
                "face_embedding": [0.1 * (i % 7) for i in range(128)],
                "fingerprint_template": "FP_TEMPLATE_ALEX_MERCER_1204",
                "is_active": True,
                "created_at": "2026-08-01T08:00:00Z"
            },
            {
                "id": "a0000000-0000-0000-0000-000000000003",
                "employee_id": "EMP-103",
                "full_name": "Elena Rostova",
                "email": "elena.rostova@example.com",
                "department": "Human Resources",
                "face_embedding": [0.03 * (i % 9) for i in range(128)],
                "fingerprint_template": "FP_TEMPLATE_ELENA_ROSTOVA_5512",
                "is_active": True,
                "created_at": "2026-08-01T08:00:00Z"
            },
            {
                "id": "a0000000-0000-0000-0000-000000000004",
                "employee_id": "EMP-104",
                "full_name": "David Vance",
                "email": "david.vance@example.com",
                "department": "Finance",
                "face_embedding": [0.08 * (i % 4) for i in range(128)],
                "fingerprint_template": "FP_TEMPLATE_DAVID_VANCE_7743",
                "is_active": True,
                "created_at": "2026-08-01T08:00:00Z"
            },
            {
                "id": "a0000000-0000-0000-0000-000000000005",
                "employee_id": "EMP-105",
                "full_name": "Marcus Wright",
                "email": "marcus.wright@example.com",
                "department": "Security",
                "face_embedding": [0.12 * (i % 3) for i in range(128)],
                "fingerprint_template": "FP_TEMPLATE_MARCUS_WRIGHT_8831",
                "is_active": True,
                "created_at": "2026-08-01T08:00:00Z"
            }
        ]
        
        self.attendance: List[Dict[str, Any]] = [
            {
                "id": "b0000000-0000-0000-0000-000000000001",
                "user_id": "a0000000-0000-0000-0000-000000000001",
                "user": self.users[0],
                "date": "2026-08-08",
                "check_in_time": "2026-08-08T08:45:00Z",
                "status": "PRESENT",
                "override_reason": None,
                "modified_by": None,
                "created_at": "2026-08-08T08:45:00Z",
                "updated_at": "2026-08-08T08:45:00Z"
            },
            {
                "id": "b0000000-0000-0000-0000-000000000002",
                "user_id": "a0000000-0000-0000-0000-000000000002",
                "user": self.users[1],
                "date": "2026-08-08",
                "check_in_time": "2026-08-08T09:22:15Z",
                "status": "LATE",
                "override_reason": None,
                "modified_by": None,
                "created_at": "2026-08-08T09:22:15Z",
                "updated_at": "2026-08-08T09:22:15Z"
            }
        ]
        
        self.audit_logs: List[Dict[str, Any]] = []

mock_db = MockDatabaseStore()
