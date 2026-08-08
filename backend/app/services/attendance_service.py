import uuid
import logging
from datetime import datetime, time, date
from typing import List, Dict, Any, Optional
from app.config import settings
from app.db import supabase, mock_db
from app.schemas import AttendanceStatus, AttendanceOverrideRequest, AttendanceOut, AuditLogOut

logger = logging.getLogger("attendance.service")

def parse_cutoff_time() -> time:
    """Parses environment CUTOFF_TIME setting (e.g. '09:00') into a datetime.time object."""
    try:
        parts = settings.CUTOFF_TIME.split(":")
        return time(int(parts[0]), int(parts[1]))
    except Exception:
        return time(9, 0)

def determine_attendance_status(scan_datetime: datetime) -> AttendanceStatus:
    """
    Core Rule: Check-in at or before 9:00 AM is PRESENT.
    Check-in after 9:00 AM is LATE.
    """
    cutoff = parse_cutoff_time()
    scan_time = scan_datetime.time()
    
    if scan_time <= cutoff:
        return AttendanceStatus.PRESENT
    else:
        return AttendanceStatus.LATE

def process_biometric_checkin(user: Dict[str, Any], scan_dt: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Records or updates a user's daily check-in.
    Enforces 9:00 AM cutoff policy.
    """
    current_dt = scan_dt if scan_dt else datetime.now()
    today_str = current_dt.strftime("%Y-%m-%d")
    iso_time_str = current_dt.isoformat()
    status = determine_attendance_status(current_dt)

    if supabase:
        try:
            # Check if user already checked in today
            existing = supabase.table("attendance").select("*").eq("user_id", user["id"]).eq("date", today_str).execute()
            if existing.data and len(existing.data) > 0:
                record = existing.data[0]
                # If existing status was ABSENT or record exists, update check-in time
                updated = supabase.table("attendance").update({
                    "check_in_time": iso_time_str,
                    "status": status.value,
                    "updated_at": iso_time_str
                }).eq("id", record["id"]).execute()
                
                return {
                    **updated.data[0],
                    "user": user
                }
            else:
                inserted = supabase.table("attendance").insert({
                    "user_id": user["id"],
                    "date": today_str,
                    "check_in_time": iso_time_str,
                    "status": status.value
                }).execute()
                
                return {
                    **inserted.data[0],
                    "user": user
                }
        except Exception as e:
            logger.error(f"Supabase checkin error: {e}. Using mock DB fallback.")

    # Mock DB Fallback
    for rec in mock_db.attendance:
        if rec["user_id"] == user["id"] and rec["date"] == today_str:
            rec["check_in_time"] = iso_time_str
            rec["status"] = status.value
            rec["updated_at"] = iso_time_str
            return rec

    new_record = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "user": user,
        "date": today_str,
        "check_in_time": iso_time_str,
        "status": status.value,
        "override_reason": None,
        "modified_by": None,
        "created_at": iso_time_str,
        "updated_at": iso_time_str
    }
    mock_db.attendance.append(new_record)
    return new_record

def fetch_attendance_list(
    query_date: Optional[str] = None, 
    status_filter: Optional[str] = None, 
    search: Optional[str] = None
) -> List[AttendanceOut]:
    """
    Fetches daily attendance records formatted for admin dashboard.
    """
    target_date = query_date if query_date else datetime.now().strftime("%Y-%m-%d")
    results: List[AttendanceOut] = []

    if supabase:
        try:
            query = supabase.table("attendance").select("*, user:users(*)").eq("date", target_date)
            if status_filter and status_filter.upper() != "ALL":
                query = query.eq("status", status_filter.upper())
            
            res = query.execute()
            if res.data:
                for row in res.data:
                    u = row.get("user") or {}
                    full_name = u.get("full_name", "Unknown")
                    emp_id = u.get("employee_id", "N/A")
                    
                    if search:
                        s = search.lower()
                        if s not in full_name.lower() and s not in emp_id.lower():
                            continue
                            
                    results.append(AttendanceOut(
                        id=row["id"],
                        user_id=row["user_id"],
                        employee_id=emp_id,
                        full_name=full_name,
                        email=u.get("email", ""),
                        department=u.get("department", "General"),
                        date=row["date"],
                        check_in_time=row.get("check_in_time"),
                        status=AttendanceStatus(row["status"]),
                        override_reason=row.get("override_reason"),
                        modified_by=row.get("modified_by"),
                        updated_at=row.get("updated_at", row.get("created_at", ""))
                    ))
                return results
        except Exception as e:
            logger.error(f"Supabase fetch attendance error: {e}. Fallback to mock store.")

    # Mock Store Fallback
    for row in mock_db.attendance:
        if row["date"] == target_date:
            u = row.get("user") or {}
            full_name = u.get("full_name", "Unknown")
            emp_id = u.get("employee_id", "N/A")

            if status_filter and status_filter.upper() != "ALL" and row["status"] != status_filter.upper():
                continue

            if search:
                s = search.lower()
                if s not in full_name.lower() and s not in emp_id.lower():
                    continue

            results.append(AttendanceOut(
                id=row["id"],
                user_id=row["user_id"],
                employee_id=emp_id,
                full_name=full_name,
                email=u.get("email", ""),
                department=u.get("department", "General"),
                date=row["date"],
                check_in_time=row.get("check_in_time"),
                status=AttendanceStatus(row["status"]),
                override_reason=row.get("override_reason"),
                modified_by=row.get("modified_by"),
                updated_at=row.get("updated_at", row.get("created_at", ""))
            ))
            
    return results

def override_attendance_status(attendance_id: str, req: AttendanceOverrideRequest) -> AttendanceOut:
    """
    Allows admin manual status edit (e.g. ABSENT -> EXCUSED or PRESENT).
    Mandates override_reason and writes immutable entry to audit_logs table.
    """
    now_str = datetime.now().isoformat()
    previous_status: Optional[str] = None
    target_record: Optional[Dict[str, Any]] = None

    if supabase:
        try:
            # 1. Fetch current record
            existing = supabase.table("attendance").select("*, user:users(*)").eq("id", attendance_id).execute()
            if existing.data and len(existing.data) > 0:
                record = existing.data[0]
                previous_status = record["status"]
                
                # 2. Update attendance
                updated = supabase.table("attendance").update({
                    "status": req.status.value,
                    "override_reason": req.override_reason,
                    "modified_by": req.admin_id,
                    "updated_at": now_str
                }).eq("id", attendance_id).execute()
                
                # 3. Create Audit Log Entry
                supabase.table("audit_logs").insert({
                    "attendance_id": attendance_id,
                    "action": "STATUS_OVERRIDE",
                    "previous_status": previous_status,
                    "new_status": req.status.value,
                    "reason": req.override_reason,
                    "performed_by": req.admin_id
                }).execute()

                u = record.get("user") or {}
                return AttendanceOut(
                    id=attendance_id,
                    user_id=record["user_id"],
                    employee_id=u.get("employee_id", "N/A"),
                    full_name=u.get("full_name", "Unknown"),
                    email=u.get("email", ""),
                    department=u.get("department", "General"),
                    date=record["date"],
                    check_in_time=record.get("check_in_time"),
                    status=req.status,
                    override_reason=req.override_reason,
                    modified_by=req.admin_id,
                    updated_at=now_str
                )
        except Exception as e:
            logger.error(f"Supabase override error: {e}. Using mock store.")

    # Mock Store Fallback
    for rec in mock_db.attendance:
        if rec["id"] == attendance_id:
            previous_status = rec["status"]
            rec["status"] = req.status.value
            rec["override_reason"] = req.override_reason
            rec["modified_by"] = req.admin_id
            rec["updated_at"] = now_str
            
            # Log audit entry
            mock_db.audit_logs.append({
                "id": str(uuid.uuid4()),
                "attendance_id": attendance_id,
                "action": "STATUS_OVERRIDE",
                "previous_status": previous_status,
                "new_status": req.status.value,
                "reason": req.override_reason,
                "performed_by": req.admin_id,
                "created_at": now_str
            })
            
            u = rec.get("user") or {}
            return AttendanceOut(
                id=attendance_id,
                user_id=rec["user_id"],
                employee_id=u.get("employee_id", "N/A"),
                full_name=u.get("full_name", "Unknown"),
                email=u.get("email", ""),
                department=u.get("department", "General"),
                date=rec["date"],
                check_in_time=rec.get("check_in_time"),
                status=req.status,
                override_reason=req.override_reason,
                modified_by=req.admin_id,
                updated_at=now_str
            )
            
    raise ValueError(f"Attendance record with ID '{attendance_id}' not found.")

def trigger_absentee_cutoff_job(target_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Automated job running daily at 9:00 AM cutoff.
    Finds all active users without a check-in record for target_date and inserts ABSENT status.
    """
    query_date = target_date if target_date else datetime.now().strftime("%Y-%m-%d")
    absent_user_ids: List[str] = []
    now_str = datetime.now().isoformat()

    if supabase:
        try:
            # 1. Fetch all active users
            users_res = supabase.table("users").select("id").eq("is_active", True).execute()
            active_users = users_res.data or []
            
            # 2. Fetch existing attendance records for target date
            attendance_res = supabase.table("attendance").select("user_id").eq("date", query_date).execute()
            checked_in_user_ids = {a["user_id"] for a in (attendance_res.data or [])}
            
            # 3. Identify users missing attendance record
            missing_users = [u for u in active_users if u["id"] not in checked_in_user_ids]
            
            # 4. Insert ABSENT records
            to_insert = [
                {
                    "user_id": u["id"],
                    "date": query_date,
                    "status": "ABSENT",
                    "override_reason": "Automated 9:00 AM System Cutoff",
                    "created_at": now_str,
                    "updated_at": now_str
                }
                for u in missing_users
            ]
            
            if to_insert:
                supabase.table("attendance").insert(to_insert).execute()
                absent_user_ids = [u["id"] for u in missing_users]

            return {
                "message": f"Successfully executed 9:00 AM cutoff job for date {query_date}.",
                "date": query_date,
                "absent_count": len(absent_user_ids),
                "processed_user_ids": absent_user_ids
            }
        except Exception as e:
            logger.error(f"Supabase cutoff job error: {e}. Executing fallback mock cutoff.")

    # Mock DB Fallback
    checked_in_ids = {rec["user_id"] for rec in mock_db.attendance if rec["date"] == query_date}
    for user in mock_db.users:
        if user["is_active"] and user["id"] not in checked_in_ids:
            new_absent_record = {
                "id": str(uuid.uuid4()),
                "user_id": user["id"],
                "user": user,
                "date": query_date,
                "check_in_time": None,
                "status": "ABSENT",
                "override_reason": "Automated 9:00 AM System Cutoff",
                "modified_by": "SYSTEM_SCHEDULER",
                "created_at": now_str,
                "updated_at": now_str
            }
            mock_db.attendance.append(new_absent_record)
            absent_user_ids.append(user["id"])

    return {
        "message": f"Successfully executed 9:00 AM cutoff job for date {query_date}.",
        "date": query_date,
        "absent_count": len(absent_user_ids),
        "processed_user_ids": absent_user_ids
    }
