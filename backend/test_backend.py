"""
Biometric Attendance Management System - Backend Verification Suite
Tests core business logic, vector similarity matching, 9 AM cutoff rules, and audit-logged manual status override logic.
"""
import unittest
from datetime import datetime
from app.schemas import BiometricScanRequest, AttendanceOverrideRequest, AttendanceStatus
from app.services.biometric_service import calculate_cosine_similarity
from app.services.attendance_service import determine_attendance_status, override_attendance_status, trigger_absentee_cutoff_job
from app.db import mock_db

class TestBiometricAttendanceCore(unittest.TestCase):
    
    def test_vector_dimension_validation(self):
        """Test that Pydantic enforces 128-d face embedding vectors."""
        valid_vec = [0.1] * 128
        req = BiometricScanRequest(face_embedding=valid_vec)
        self.assertEqual(len(req.face_embedding), 128)
        
        invalid_vec = [0.1] * 100
        with self.assertRaises(ValueError):
            BiometricScanRequest(face_embedding=invalid_vec)

    def test_cosine_similarity_numpy(self):
        """Test Cosine Similarity algorithm produces expected float scores."""
        vec1 = [1.0] + [0.0] * 127
        vec2 = [1.0] + [0.0] * 127
        score_identical = calculate_cosine_similarity(vec1, vec2)
        self.assertAlmostEqual(score_identical, 1.0, places=4)
        
        vec3 = [0.0] * 127 + [1.0]
        score_orthogonal = calculate_cosine_similarity(vec1, vec3)
        self.assertAlmostEqual(score_orthogonal, 0.0, places=4)

    def test_9am_cutoff_time_rules(self):
        """Test rule: Scan at or before 9:00 AM is PRESENT. After 9:00 AM is LATE."""
        time_before = datetime.strptime("2026-08-08 08:59:59", "%Y-%m-%d %H:%M:%S")
        status_before = determine_attendance_status(time_before)
        self.assertEqual(status_before, AttendanceStatus.PRESENT)

        time_exact = datetime.strptime("2026-08-08 09:00:00", "%Y-%m-%d %H:%M:%S")
        status_exact = determine_attendance_status(time_exact)
        self.assertEqual(status_exact, AttendanceStatus.PRESENT)

        time_after = datetime.strptime("2026-08-08 09:00:01", "%Y-%m-%d %H:%M:%S")
        status_after = determine_attendance_status(time_after)
        self.assertEqual(status_after, AttendanceStatus.LATE)

    def test_override_mandates_reason_and_logs_audit(self):
        """Test manual admin status override mandates non-empty reason and logs to audit_logs."""
        # Test override on existing mock record b0000000-0000-0000-0000-000000000002 (LATE -> EXCUSED)
        rec_id = "b0000000-0000-0000-0000-000000000002"
        override_req = AttendanceOverrideRequest(
            status=AttendanceStatus.EXCUSED,
            override_reason="Medical Leave Certificate Submitted #ML-9921",
            admin_id="ADMIN-SYS-99"
        )
        
        initial_logs_count = len(mock_db.audit_logs)
        updated_record = override_attendance_status(rec_id, override_req)
        
        self.assertEqual(updated_record.status, AttendanceStatus.EXCUSED)
        self.assertEqual(updated_record.override_reason, "Medical Leave Certificate Submitted #ML-9921")
        self.assertEqual(updated_record.modified_by, "ADMIN-SYS-99")
        
        # Verify audit log recorded
        self.assertEqual(len(mock_db.audit_logs), initial_logs_count + 1)
        latest_audit = mock_db.audit_logs[-1]
        self.assertEqual(latest_audit["attendance_id"], rec_id)
        self.assertEqual(latest_audit["previous_status"], "LATE")
        self.assertEqual(latest_audit["new_status"], "EXCUSED")
        self.assertEqual(latest_audit["performed_by"], "ADMIN-SYS-99")

    def test_trigger_absentee_cutoff_job(self):
        """Test 9:00 AM automated job inserts ABSENT status for unrecorded users."""
        res = trigger_absentee_cutoff_job(target_date="2026-08-08")
        self.assertIn("Successfully executed", res["message"])
        self.assertGreaterEqual(res["absent_count"], 1)

if __name__ == "__main__":
    unittest.main()
