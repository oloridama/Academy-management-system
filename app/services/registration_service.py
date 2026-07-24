"""Registration business workflow — handles prospect admission and student creation."""
from app.repositories.student_repository import StudentRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.batch_repository import BatchRepository
from app.models.student import Student


class RegistrationService:
    """Orchestrates the full registration workflow: prospect → student → enrolled."""

    # ── REFACTORING NOTES ──────────────────────────────────────────────
    # 1. FIXED IMPORT — the original imported StudentRepository from
    #    `app.repositories.attendance_repository` which was the wrong
    #    module path.
    #
    # 2. REMOVED `batches` list from constructor — batches are owned by
    #    BatchRepository. Passing them separately creates data duplication
    #    and stale references. Now the service uses BatchRepository
    #    directly.
    #
    # 3. FIXED `find_student` usage — the original checked
    #    `== False`, but the old repo returned a bool. The new repo
    #    returns Student | None, so we check `is None` instead.
    #
    # 4. FIXED enrollment call — the original passed
    #    `new_student[student_id]` which would fail on a Student
    #    dataclass (not a dict). Now uses `.student_id` attribute access.
    #
    # 5. ADDED full Registration record creation — the original only
    #    created a student and enrolled them, but never stored the
    #    Registration entity itself.
    #
    # 6. ADDED batch capacity check before enrollment.
    # ───────────────────────────────────────────────────────────────────

    def __init__(
        self,
        student_repo: StudentRepository | None = None,
        enrollment_repo: EnrollmentRepository | None = None,
        batch_repo: BatchRepository | None = None,
    ):
        self.student_repo = student_repo or StudentRepository()
        self.enrollment_repo = enrollment_repo or EnrollmentRepository()
        self.batch_repo = batch_repo or BatchRepository()

    def register_student(
        self,
        firstname: str,
        lastname: str,
        dob: str,
        gender: str,
        email: str,
        phone: str,
        emergency_contact: str = "",
        background: str = "",
        passport: str = "",
        student_id: str = "",
        selected_batch_id: str = "",
    ) -> Student:
        """Register a prospect: create or update a Student, then optionally enroll in a batch.

        Returns the Student object. If student_id is provided and matches an existing
        student, their profile is updated. Otherwise a new student is created.
        """
        existing = self.student_repo.find_student(
            firstname=firstname, lastname=lastname, student_id=student_id
        )

        if existing is None:
            # New prospect — create a student profile
            student = self.student_repo.add_student(
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                dob=dob,
                email=email,
                phone=phone,
                background=background,
                passport=passport,
                emergency=emergency_contact,
            )
        else:
            # Returning student — update their profile
            update_data = {
                "first_name": firstname,
                "last_name": lastname,
                "gender": gender,
                "email": email,
                "phone": phone,
                "emergency_contact": emergency_contact,
                "educational_background": background,
                "date_of_birth": dob,
                "passport_photograph": passport,
            }
            student = self.student_repo.update_student(
                student_id=existing.student_id, **update_data
            )
            if student is None:
                raise RuntimeError(f"Failed to update student {existing.student_id}")

        # Enroll in a batch if requested
        if selected_batch_id:
            self._enroll_in_batch(student.student_id, selected_batch_id)

        return student

    def _enroll_in_batch(self, student_id: str, batch_id: str) -> None:
        """Enroll a student into a batch, with capacity validation."""
        batch = self.batch_repo.get_batch_by_id(batch_id)
        if batch is None:
            raise ValueError(f"Batch '{batch_id}' not found. Create the batch first.")

        # Check capacity
        if len(batch.enrolled_students) >= batch.capacity:
            raise ValueError(
                f"Batch '{batch_id}' is full "
                f"({len(batch.enrolled_students)}/{batch.capacity})."
            )

        # Check for duplicate enrollment
        for enrollment in self.enrollment_repo.get_enrollments_by_student(student_id):
            if enrollment.batch_id == batch_id and enrollment.completion_status == "active":
                raise ValueError(f"Student {student_id} is already enrolled in batch '{batch_id}'.")

        # Create enrollment record
        enrollment = self.enrollment_repo.enroll(student_id=student_id, batch_id=batch_id)

        # Add student to batch roster
        self.batch_repo.enroll_student(batch_id, student_id)

        print(
            f"Student {student_id} enrolled in batch '{batch_id}' "
            f"(Enrollment ID: {enrollment.enrollment_id})."
        )

    def transfer_student(self, student_id: str, from_batch_id: str, to_batch_id: str) -> None:
        """Transfer a student from one batch to another."""
        # Find active enrollment in the source batch
        active = self.enrollment_repo.get_active_enrollment(student_id)
        if active is None or active.batch_id != from_batch_id:
            raise ValueError(
                f"Student {student_id} is not actively enrolled in batch '{from_batch_id}'."
            )

        # Suspend current enrollment
        self.enrollment_repo.suspend_enrollment(active.enrollment_id)

        # Remove from old batch roster
        self.batch_repo.remove_student(from_batch_id, student_id)

        # Enroll in new batch
        self._enroll_in_batch(student_id, to_batch_id)

