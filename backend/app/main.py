import logging
from contextlib import asynccontextmanager
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.scheduler import start_scheduler, stop_scheduler
from app.schemas import (
    BiometricScanRequest, 
    ScanResponse, 
    AttendanceOut, 
    AttendanceOverrideRequest, 
    CutoffJobResult,
    UserOut
)
from app.services.biometric_service import match_biometric_data
from app.services.attendance_service import (
    process_biometric_checkin, 
    fetch_attendance_list, 
    override_attendance_status, 
    trigger_absentee_cutoff_job
)
from app.db import mock_db, supabase

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("attendance.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to handle startup and shutdown events."""
    logger.info("Initializing Biometric Attendance System API Server...")
    start_scheduler()
    yield
    logger.info("Shutting down API Server...")
    stop_scheduler()

app = FastAPI(
    title="Biometric Attendance Management System API",
    description="High-performance backend API with FastAPI, Supabase pgvector, NumPy vector comparison, and APScheduler daily 9:00 AM cutoff automation.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Vue 3 SPA frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "database": "supabase" if supabase else "mock_in_memory",
        "cutoff_time": settings.CUTOFF_TIME,
        "face_threshold": settings.FACE_MATCH_THRESHOLD
    }

# --------------------------------------------------------------------
# BIOMETRIC ENDPOINTS
# --------------------------------------------------------------------
@app.post(
    "/api/v1/biometric/scan", 
    response_model=ScanResponse, 
    summary="Process facial or fingerprint biometric scan",
    tags=["Biometric Scanner"]
)
def biometric_scan(scan_request: BiometricScanRequest):
    """
    Receives 128-d face embedding vector or fingerprint template hash from biometric hardware unit.
    - Matches biometric template against registered active users.
    - Checks current check-in time against 9:00 AM cutoff rule (Before 9 AM -> PRESENT, After 9 AM -> LATE).
    - Updates database attendance record.
    """
    try:
        user, score, match_method = match_biometric_data(scan_request)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Biometric matching failed. Score ({score:.2f}) below threshold ({settings.FACE_MATCH_THRESHOLD}). No user record matched."
            )

        attendance_record = process_biometric_checkin(user, scan_dt=scan_request.scan_time)
        
        return ScanResponse(
            success=True,
            message=f"Biometric check-in verified via {match_method} (Score: {score:.2f}).",
            user_id=user["id"],
            employee_id=user["employee_id"],
            user_name=user["full_name"],
            check_in_time=attendance_record.get("check_in_time", ""),
            status=attendance_record["status"],
            similarity_score=round(score, 4)
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Error processing scan: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal biometric verification error: {str(e)}")

# --------------------------------------------------------------------
# ATTENDANCE MANAGEMENT ENDPOINTS
# --------------------------------------------------------------------
@app.get(
    "/api/v1/attendance", 
    response_model=List[AttendanceOut],
    summary="Get daily attendance records for admin portal",
    tags=["Attendance Admin"]
)
def get_attendance(
    date: Optional[str] = Query(None, description="Query date in YYYY-MM-DD format (defaults to current date)"),
    status: Optional[str] = Query(None, description="Filter status (PRESENT, ABSENT, EXCUSED, LATE, ALL)"),
    search: Optional[str] = Query(None, description="Search employee name or ID")
):
    """
    Retrieves daily attendance records for the Vue 3 admin dashboard table.
    """
    return fetch_attendance_list(query_date=date, status_filter=status, search=search)

@app.post(
    "/api/v1/attendance/{attendance_id}/override",
    response_model=AttendanceOut,
    summary="Admin override of attendance status",
    tags=["Attendance Admin"]
)
def override_attendance(attendance_id: str, override_request: AttendanceOverrideRequest):
    """
    Allows authenticated admin personnel to manually override an attendance status (e.g. ABSENT -> EXCUSED or PRESENT).
    Requires mandatory `override_reason` text field.
    Logs audit entry into `audit_logs` table.
    """
    try:
        return override_attendance_status(attendance_id, override_request)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        logger.error(f"Error executing status override: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post(
    "/api/v1/scheduler/trigger-cutoff",
    response_model=CutoffJobResult,
    summary="Manually trigger 9:00 AM cutoff job",
    tags=["Scheduler Automation"]
)
def manual_trigger_cutoff(target_date: Optional[str] = Query(None, description="Target date YYYY-MM-DD")):
    """
    Manually triggers the 9:00 AM cutoff job to check for missing user scans and set status to ABSENT.
    Useful for demonstration, manual admin triggers, or integration testing.
    """
    return trigger_absentee_cutoff_job(target_date=target_date)

@app.get(
    "/api/v1/users",
    response_model=List[UserOut],
    summary="List all registered system users",
    tags=["User Management"]
)
def get_users():
    """Returns list of registered users."""
    if supabase:
        try:
            res = supabase.table("users").select("*").execute()
            if res.data:
                return res.data
        except Exception:
            pass
    return mock_db.users

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
