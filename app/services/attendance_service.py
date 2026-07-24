"""Attendance business workflow — handles attendance recording and queries."""
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.batch_repository import BatchRepository
from app.models.attendance import AttendanceRecord, BatchSessionAttendance


class AttendanceService:
    """Orchestrates attendance marking, tracking, and reporting."""

    def __init__(
        self,
        attendance_repo: AttendanceRepository | None = None,
        batch_repo: BatchRepository | None = None,
    ):
        self.attendance_repo = attendance_repo or AttendanceRepository()
        self.batch_repo = batch_repo or BatchRepository()

    def mark_student_present(
        self,
        first_name: str,
        last_name: str,
        date: str,
        batch_id: str,
    ) -> AttendanceRecord:
        """Mark a student as present for a given date and batch."""
        return self.attendance_repo.mark_attendance(
            first_name=first_name,
            last_name=last_name,
            date=date,
            batch_id=batch_id,
            is_present=True,
            role="student",
        )

    def mark_student_absent(
        self,
        first_name: str,
        last_name: str,
        date: str,
        batch_id: str,
    ) -> AttendanceRecord:
        """Mark a student as absent for a given date and batch."""
        return self.attendance_repo.mark_attendance(
            first_name=first_name,
            last_name=last_name,
            date=date,
            batch_id=batch_id,
            is_present=False,
            role="student",
        )

    def mark_instructor_present(
        self,
        first_name: str,
        last_name: str,
        date: str,
        batch_id: str,
    ) -> AttendanceRecord:
        """Mark an instructor as present for a given date and batch."""
        return self.attendance_repo.mark_attendance(
            first_name=first_name,
            last_name=last_name,
            date=date,
            batch_id=batch_id,
            is_present=True,
            role="instructor",
        )

    def record_session_attendance(
        self,
        date: str,
        batch_id: str,
        lesson_topic: str = "",
        present_student_ids: list[str] | None = None,
        present_instructor_ids: list[str] | None = None,
    ) -> BatchSessionAttendance:
        """Create a session-level attendance summary with auto-calculated absent count."""
        batch = self.batch_repo.get_batch_by_id(batch_id)
        total_enrolled = len(batch.enrolled_students) if batch else 0

        return self.attendance_repo.create_session_attendance(
            date=date,
            batch_id=batch_id,
            lesson_topic=lesson_topic,
            present_student_ids=present_student_ids,
            present_instructor_ids=present_instructor_ids,
            total_enrolled=total_enrolled,
        )

    def get_student_absent_dates(
        self, first_name: str, last_name: str, batch_id: str = ""
    ) -> list[str]:
        """Get all dates a student was marked absent."""
        return self.attendance_repo.get_absent_dates(first_name, last_name, batch_id)

    def get_student_absent_count(
        self, first_name: str, last_name: str, batch_id: str = ""
    ) -> int:
        """Get the number of days a student was absent."""
        return self.attendance_repo.get_days_absent(first_name, last_name, batch_id)

    def get_session_summary(
        self, batch_id: str, date: str
    ) -> BatchSessionAttendance | None:
        """Get the attendance summary for a specific batch session."""
        return self.attendance_repo.get_session_by_date(batch_id, date)

    def get_all_sessions(self) -> list[BatchSessionAttendance]:
        """Return all session attendance summaries."""
        return self.attendance_repo.get_all_sessions()

    def get_all_records(self) -> list[AttendanceRecord]:
        """Return all individual attendance records."""
        return self.attendance_repo.get_all_records()