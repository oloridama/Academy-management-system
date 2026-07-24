"""Enrollment business workflow — handles student enrollment management."""
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.batch_repository import BatchRepository
from app.models.enrollment import Enrollment


class EnrollmentService:
    """Orchestrates enrollment operations across batches."""

    # ── REFACTORING NOTES ──────────────────────────────────────────────
    # 1. REMOVED `EnrollmentRepository(batch=batch_id)` — the old repo
    #    was tied to a single batch. The new repo takes no args; batch
    #    is passed per operation.
    #
    # 2. ADDED BatchRepository dependency — needed for capacity checks
    #    and roster management.
    #
    # 3. ADDED full enrollment lifecycle methods: pay, suspend, drop,
    #    complete — the original only had `enroll_student`.
    # ───────────────────────────────────────────────────────────────────

    def __init__(
        self,
        enrollment_repo: EnrollmentRepository | None = None,
        batch_repo: BatchRepository | None = None,
    ):
        self.enrollment_repo = enrollment_repo or EnrollmentRepository()
        self.batch_repo = batch_repo or BatchRepository()

    def enroll_student(self, student_id: str, batch_id: str) -> Enrollment:
        """Enroll a student into a batch, with capacity and duplicate checks."""
        batch = self.batch_repo.get_batch_by_id(batch_id)
        if batch is None:
            raise ValueError(f"Batch '{batch_id}' not found.")

        if len(batch.enrolled_students) >= batch.capacity:
            raise ValueError(
                f"Batch '{batch_id}' is full "
                f"({len(batch.enrolled_students)}/{batch.capacity})."
            )

        # Duplicate check
        for e in self.enrollment_repo.get_enrollments_by_student(student_id):
            if e.batch_id == batch_id and e.completion_status == "active":
                raise ValueError(
                    f"Student '{student_id}' is already enrolled in batch '{batch_id}'."
                )

        enrollment = self.enrollment_repo.enroll(student_id, batch_id)
        self.batch_repo.enroll_student(batch_id, student_id)
        return enrollment

    def make_payment(self, enrollment_id: str) -> Enrollment:
        """Mark an enrollment as paid."""
        enrollment = self.enrollment_repo.update_payment_status(enrollment_id, "paid")
        if enrollment is None:
            raise ValueError(f"Enrollment '{enrollment_id}' not found.")
        return enrollment

    def suspend_enrollment(self, enrollment_id: str) -> Enrollment:
        """Suspend an active enrollment."""
        enrollment = self.enrollment_repo.suspend_enrollment(enrollment_id)
        if enrollment is None:
            raise ValueError(f"Enrollment '{enrollment_id}' not found.")
        return enrollment

    def drop_enrollment(self, enrollment_id: str, batch_id: str, student_id: str) -> None:
        """Drop a student from a batch entirely."""
        enrollment = self.enrollment_repo.update_enrollment(
            enrollment_id, completion_status="dropped"
        )
        if enrollment is None:
            raise ValueError(f"Enrollment '{enrollment_id}' not found.")
        self.batch_repo.remove_student(batch_id, student_id)

    def complete_enrollment(self, enrollment_id: str) -> Enrollment:
        """Mark an enrollment as completed (graduated)."""
        enrollment = self.enrollment_repo.mark_completed(enrollment_id)
        if enrollment is None:
            raise ValueError(f"Enrollment '{enrollment_id}' not found.")
        return enrollment

    def get_student_enrollments(self, student_id: str) -> list[Enrollment]:
        """Get all enrollment records for a student."""
        return self.enrollment_repo.get_enrollments_by_student(student_id)

    def get_batch_enrollments(self, batch_id: str) -> list[Enrollment]:
        """Get all enrollment records for a batch."""
        return self.enrollment_repo.get_enrollments_by_batch(batch_id)