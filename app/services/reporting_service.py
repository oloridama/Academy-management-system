"""Reporting business workflow — generates institution-wide reports."""
from dataclasses import dataclass, field
from app.repositories.student_repository import StudentRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.batch_repository import BatchRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.instructor_repository import InstructorRepository


@dataclass
class EnrollmentReport:
    """Summary report for enrollments."""
    total_enrollments: int = 0
    active_enrollments: int = 0
    completed_enrollments: int = 0
    suspended_enrollments: int = 0
    dropped_enrollments: int = 0


@dataclass
class AttendanceReport:
    """Summary report for attendance."""
    total_records: int = 0
    total_sessions: int = 0
    total_present: int = 0
    total_absent: int = 0


@dataclass
class AcademyOverview:
    """Top-level summary of the entire academy."""
    total_students: int = 0
    total_instructors: int = 0
    total_courses: int = 0
    total_batches: int = 0
    active_batches: int = 0
    enrollments: EnrollmentReport = field(default_factory=EnrollmentReport)
    attendance: AttendanceReport = field(default_factory=AttendanceReport)


class ReportingService:
    """Generates reports across all academy domains."""

    def __init__(
        self,
        student_repo: StudentRepository | None = None,
        enrollment_repo: EnrollmentRepository | None = None,
        attendance_repo: AttendanceRepository | None = None,
        batch_repo: BatchRepository | None = None,
        course_repo: CourseRepository | None = None,
        instructor_repo: InstructorRepository | None = None,
    ):
        self.student_repo = student_repo or StudentRepository()
        self.enrollment_repo = enrollment_repo or EnrollmentRepository()
        self.attendance_repo = attendance_repo or AttendanceRepository()
        self.batch_repo = batch_repo or BatchRepository()
        self.course_repo = course_repo or CourseRepository()
        self.instructor_repo = instructor_repo or InstructorRepository()

    def get_academy_overview(self) -> AcademyOverview:
        """Generate a top-level summary of the academy."""
        batches = self.batch_repo.get_all_batches()
        enrollments = self.enrollment_repo.get_all_enrollments()
        records = self.attendance_repo.get_all_records()

        # Enrollment breakdown
        enrollment_report = EnrollmentReport(
            total_enrollments=len(enrollments),
            active_enrollments=sum(
                1 for e in enrollments if e.completion_status == "active"
            ),
            completed_enrollments=sum(
                1 for e in enrollments if e.completion_status == "completed"
            ),
            suspended_enrollments=sum(
                1 for e in enrollments if e.completion_status == "suspended"
            ),
            dropped_enrollments=sum(
                1 for e in enrollments if e.completion_status == "dropped"
            ),
        )

        # Attendance breakdown
        attendance_report = AttendanceReport(
            total_records=len(records),
            total_sessions=len(self.attendance_repo.get_all_sessions()),
            total_present=sum(1 for r in records if r.is_present),
            total_absent=sum(1 for r in records if not r.is_present),
        )

        return AcademyOverview(
            total_students=len(self.student_repo.get_all_students()),
            total_instructors=len(self.instructor_repo.get_all_instructors()),
            total_courses=len(self.course_repo.get_all_courses()),
            total_batches=len(batches),
            active_batches=sum(1 for b in batches if b.status == "active"),
            enrollments=enrollment_report,
            attendance=attendance_report,
        )

    def get_student_report(self, student_id: str) -> dict:
        """Generate a detailed report for a single student."""
        student = self.student_repo.get_student_by_id(student_id)
        if student is None:
            raise ValueError(f"Student '{student_id}' not found.")

        enrollments = self.enrollment_repo.get_enrollments_by_student(student_id)
        attendance_records = self.attendance_repo.get_records_by_person(
            student.first_name, student.last_name
        )

        return {
            "student": student,
            "enrollments": enrollments,
            "attendance_records": attendance_records,
            "days_present": sum(1 for r in attendance_records if r.is_present),
            "days_absent": sum(1 for r in attendance_records if not r.is_present),
        }

    def print_overview(self) -> None:
        """Print the academy overview to the console."""
        overview = self.get_academy_overview()
        print("=" * 50)
        print("ACADEMY MANAGEMENT SYSTEM — OVERVIEW")
        print("=" * 50)
        print(f"Total Students:     {overview.total_students}")
        print(f"Total Instructors:  {overview.total_instructors}")
        print(f"Total Courses:      {overview.total_courses}")
        print(f"Total Batches:      {overview.total_batches}")
        print(f"Active Batches:     {overview.active_batches}")
        print("-" * 50)
        print("ENROLLMENTS")
        print(f"  Total:            {overview.enrollments.total_enrollments}")
        print(f"  Active:           {overview.enrollments.active_enrollments}")
        print(f"  Completed:        {overview.enrollments.completed_enrollments}")
        print(f"  Suspended:        {overview.enrollments.suspended_enrollments}")
        print(f"  Dropped:          {overview.enrollments.dropped_enrollments}")
        print("-" * 50)
        print("ATTENDANCE")
        print(f"  Total Records:    {overview.attendance.total_records}")
        print(f"  Total Sessions:   {overview.attendance.total_sessions}")
        print(f"  Present:          {overview.attendance.total_present}")
        print(f"  Absent:           {overview.attendance.total_absent}")
        print("=" * 50)