"""Attendance data access layer."""
from app.models.attendance import AttendanceRecord, BatchSessionAttendance


class AttendanceRepository:
    """Manages attendance records for students and instructors."""

    # ── REFACTORING NOTES ──────────────────────────────────────────────
    # 1. SIMPLIFIED CONSTRUCTOR — the original took 7 parameters
    #    (attendance type, day, month, year, session_days, breaks,
    #    general_calendar) and tried to build a full academic calendar
    #    at init time. This conflated attendance recording with calendar
    #    management. Now the repository is focused solely on storing and
    #    querying attendance records.
    #
    # 2. REMOVED calendar/session logic — belongs in a separate utility
    #    or service, not the data layer.
    #
    # 3. REMOVED dependency on StudentRepository/InstructorRepository —
    #    the original instantiated both with no constructor args
    #    (causing TypeError). The attendance repo should not own student
    #    or instructor data.
    #
    # 4. REPLACED the complex nested dict structure with flat lists of
    #    dataclass instances — easier to query, serialize, and maintain.
    #
    # 5. FIXED TYPO: `self.atttendance_list` → proper naming.
    #
    # 6. SEPARATED individual records from session summaries —
    #    `AttendanceRecord` for per-person marks, `BatchSessionAttendance`
    #    for per-session roll-ups.
    # ───────────────────────────────────────────────────────────────────

    def __init__(self):
        self.records: list[AttendanceRecord] = []
        self.sessions: list[BatchSessionAttendance] = []

    def mark_attendance(
        self,
        first_name: str,
        last_name: str,
        date: str,
        batch_id: str,
        is_present: bool = True,
        role: str = "student",
    ) -> AttendanceRecord:
        """Record a single attendance mark for one person on one date."""
        record = AttendanceRecord(
            first_name=first_name,
            last_name=last_name,
            date=date,
            batch_id=batch_id,
            is_present=is_present,
            role=role,
        )
        self.records.append(record)
        return record

    def create_session_attendance(
        self,
        date: str,
        batch_id: str,
        lesson_topic: str = "",
        present_student_ids: list[str] | None = None,
        present_instructor_ids: list[str] | None = None,
        total_enrolled: int = 0,
    ) -> BatchSessionAttendance:
        """Create a session-level attendance summary."""
        session = BatchSessionAttendance(
            date=date,
            batch_id=batch_id,
            lesson_topic=lesson_topic,
            present_student_ids=present_student_ids if present_student_ids is not None else [],
            present_instructor_ids=present_instructor_ids if present_instructor_ids is not None else [],
            total_enrolled=total_enrolled,
        )
        self.sessions.append(session)
        return session

    def get_records_by_date(self, date: str) -> list[AttendanceRecord]:
        """Get all attendance records for a specific date."""
        return [r for r in self.records if r.date == date]

    def get_records_by_batch(self, batch_id: str) -> list[AttendanceRecord]:
        """Get all attendance records for a specific batch."""
        return [r for r in self.records if r.batch_id == batch_id]

    def get_records_by_person(self, first_name: str, last_name: str) -> list[AttendanceRecord]:
        """Get all attendance records for a specific person."""
        return [
            r for r in self.records
            if r.first_name.lower() == first_name.lower()
            and r.last_name.lower() == last_name.lower()
        ]

    def get_absent_dates(
        self, first_name: str, last_name: str, batch_id: str = ""
    ) -> list[str]:
        """Get all dates a person was marked absent."""
        records = self.get_records_by_person(first_name, last_name)
        if batch_id:
            records = [r for r in records if r.batch_id == batch_id]
        return [r.date for r in records if not r.is_present]

    def get_days_absent(
        self, first_name: str, last_name: str, batch_id: str = ""
    ) -> int:
        """Count the number of days a person was absent."""
        return len(self.get_absent_dates(first_name, last_name, batch_id))

    def get_session_by_date(self, batch_id: str, date: str) -> BatchSessionAttendance | None:
        """Get a session summary for a specific batch and date."""
        for session in self.sessions:
            if session.batch_id == batch_id and session.date == date:
                return session
        return None

    def get_all_sessions(self) -> list[BatchSessionAttendance]:
        """Return all session attendance summaries."""
        return self.sessions

    def get_all_records(self) -> list[AttendanceRecord]:
        """Return all individual attendance records."""
        return self.records