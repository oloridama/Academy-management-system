"""Enrollment data access layer."""
from app.models.enrollment import Enrollment


class EnrollmentRepository:
    """Manages CRUD operations for Enrollment entities."""

    # ── REFACTORING NOTES ──────────────────────────────────────────────
    # 1. REMOVED `batch: type[Batch]` constructor parameter — tying the
    #    entire repository to a single batch prevented it from managing
    #    enrollments across multiple batches. Now the batch reference is
    #    passed per-operation.
    #
    # 2. FIXED IMPORT: `from student_repository import ...` → proper
    #    absolute import. The original relative import without package
    #    context would fail at runtime.
    #
    # 3. `enroll()` now creates an Enrollment dataclass and stores it
    #    in a list. The original appended to `batch.enrolled_students`
    #    inside a loop over existing students, enrolling the new student
    #    once per existing student (N times).
    #
    # 4. ADDED `get_enrollments_by_student`, `get_enrollments_by_batch`,
    #    `update_enrollment` — needed for service-layer workflows like
    #    transfers and status changes.
    # ───────────────────────────────────────────────────────────────────

    def __init__(self):
        self.enrollments: list[Enrollment] = []
        self._next_id: int = 1

    def enroll(self, student_id: str, batch_id: str) -> Enrollment:
        """Create a new enrollment record for a student in a batch."""
        enrollment_id = f"ENR{self._next_id:04d}"
        self._next_id += 1

        enrollment = Enrollment(
            enrollment_id=enrollment_id,
            student_id=student_id,
            batch_id=batch_id,
        )
        self.enrollments.append(enrollment)
        return enrollment

    def get_enrollment_by_id(self, enrollment_id: str) -> Enrollment | None:
        """Find an enrollment by its ID."""
        for enrollment in self.enrollments:
            if enrollment.enrollment_id == enrollment_id:
                return enrollment
        return None

    def get_enrollments_by_student(self, student_id: str) -> list[Enrollment]:
        """Get all enrollments for a given student."""
        return [e for e in self.enrollments if e.student_id == student_id]

    def get_enrollments_by_batch(self, batch_id: str) -> list[Enrollment]:
        """Get all enrollments for a given batch."""
        return [e for e in self.enrollments if e.batch_id == batch_id]

    def get_active_enrollment(self, student_id: str) -> Enrollment | None:
        """Get the currently active enrollment for a student."""
        for enrollment in self.enrollments:
            if enrollment.student_id == student_id and enrollment.completion_status == "active":
                return enrollment
        return None

    def update_enrollment(self, enrollment_id: str, **kwargs) -> Enrollment | None:
        """Update an enrollment's fields (e.g., payment status, completion status)."""
        enrollment = self.get_enrollment_by_id(enrollment_id)
        if enrollment is None:
            return None
        for key, value in kwargs.items():
            if hasattr(enrollment, key):
                setattr(enrollment, key, value)
        return enrollment

    def update_payment_status(self, enrollment_id: str, status: str) -> Enrollment | None:
        """Update payment status (unpaid → paid → refunded)."""
        return self.update_enrollment(enrollment_id, payment_status=status)

    def mark_completed(self, enrollment_id: str) -> Enrollment | None:
        """Mark an enrollment as completed."""
        return self.update_enrollment(enrollment_id, completion_status="completed")

    def suspend_enrollment(self, enrollment_id: str) -> Enrollment | None:
        """Suspend an enrollment."""
        return self.update_enrollment(enrollment_id, completion_status="suspended")

    def get_all_enrollments(self) -> list[Enrollment]:
        """Return all enrollment records."""
        return self.enrollments