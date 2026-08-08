from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from enum import Enum
from datetime import date, datetime

class AttendanceStatus(str, Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    EXCUSED = "EXCUSED"
    LATE = "LATE"

class BiometricScanRequest(BaseModel):
    face_embedding: Optional[List[float]] = Field(
        None, 
        description="128-dimensional floating point vector representation of user face."
    )
    fingerprint_template: Optional[str] = Field(
        None, 
        description="Base64 encoded string or hash of fingerprint template."
    )
    scan_time: Optional[datetime] = Field(
        None,
        description="Optional explicit scan timestamp (defaults to current server time)."
    )

    @field_validator("face_embedding")
    @classmethod
    def validate_face_vector_length(cls, v):
        if v is not None and len(v) != 128:
            raise ValueError(f"Face vector embedding must have exactly 128 dimensions (got {len(v)}).")
        return v

class ScanResponse(BaseModel):
    success: bool
    message: str
    user_id: str
    employee_id: str
    user_name: str
    check_in_time: str
    status: AttendanceStatus
    similarity_score: float

class AttendanceOverrideRequest(BaseModel):
    status: AttendanceStatus = Field(..., description="New target attendance status (PRESENT, EXCUSED, ABSENT, LATE)")
    override_reason: str = Field(..., min_length=3, description="Mandatory detailed reason for manual admin override.")
    admin_id: Optional[str] = Field("ADMIN-001", description="User ID of the admin performing the override.")

class AttendanceOut(BaseModel):
    id: str
    user_id: str
    employee_id: str
    full_name: str
    email: str
    department: str
    date: str
    check_in_time: Optional[str] = None
    status: AttendanceStatus
    override_reason: Optional[str] = None
    modified_by: Optional[str] = None
    updated_at: str

class AuditLogOut(BaseModel):
    id: str
    attendance_id: str
    action: str
    previous_status: Optional[AttendanceStatus] = None
    new_status: AttendanceStatus
    reason: str
    performed_by: Optional[str] = None
    created_at: str

class CutoffJobResult(BaseModel):
    message: str
    date: str
    absent_count: int
    processed_user_ids: List[str]

class UserOut(BaseModel):
    id: str
    employee_id: str
    full_name: str
    email: str
    department: str
    fingerprint_template: Optional[str] = None
    is_active: bool
    created_at: str
