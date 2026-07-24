"""Batch data access layer."""
from app.models.batch import Batch


class BatchRepository:
    """Manages CRUD operations for Batch entities."""

    # ── REFACTORING NOTES ──────────────────────────────────────────────
    # 1. REMOVED `@staticmethod` — the original had `@staticmethod` on
    #    `create_batch` while the method used `self`. These are mutually
    #    exclusive: a staticmethod can't access `self`. Now it's a
    #    regular instance method.
    #
    # 2. `create_batch` now matches the updated Batch model (includes
    #    `course_id`, `schedule`, and uses `list[str]` for enrolled
    #    students/instructors).
    #
    # 3. ADDED `get_batch_by_id`, `get_all_batches`,
    #    `get_batches_by_status`, `update_batch` — the original only
    #    had create, missing essential retrieval and update operations
    #    needed by services.
    #
    # 4. ADDED `enroll_student` and `remove_student` as convenience
    #    methods directly on the repository.
    # ───────────────────────────────────────────────────────────────────

    def __init__(self):
        self.batches: list[Batch] = []

    def create_batch(
        self,
        batch_id: str,
        course_id: str,
        course_name: str,
        start_date: str,
        end_date: str,
        capacity: int = 0,
        schedule: str = "",
        instructors: list[str] | None = None,
        status: str = "upcoming",
    ) -> Batch:
        """Create a new batch for a course."""
        batch = Batch(
            batch_id=batch_id,
            course_id=course_id,
            course_name=course_name,
            start_date=start_date,
            end_date=end_date,
            capacity=capacity,
            schedule=schedule,
            instructors=instructors if instructors is not None else [],
            status=status,
        )
        self.batches.append(batch)
        return batch

    def get_batch_by_id(self, batch_id: str) -> Batch | None:
        """Find a batch by its ID."""
        for batch in self.batches:
            if batch.batch_id == batch_id:
                return batch
        return None

    def get_all_batches(self) -> list[Batch]:
        """Return all batches."""
        return self.batches

    def get_batches_by_status(self, status: str) -> list[Batch]:
        """Return batches filtered by status (upcoming/active/completed)."""
        return [b for b in self.batches if b.status.lower() == status.lower()]

    def update_batch(self, batch_id: str, **kwargs) -> Batch | None:
        """Update a batch's fields."""
        batch = self.get_batch_by_id(batch_id)
        if batch is None:
            return None
        for key, value in kwargs.items():
            if hasattr(batch, key):
                setattr(batch, key, value)
        return batch

    def enroll_student(self, batch_id: str, student_id: str) -> bool:
        """Add a student to a batch's enrolled list."""
        batch = self.get_batch_by_id(batch_id)
        if batch is None:
            return False
        if len(batch.enrolled_students) >= batch.capacity:
            return False  # batch is full
        if student_id not in batch.enrolled_students:
            batch.enrolled_students.append(student_id)
        return True

    def remove_student(self, batch_id: str, student_id: str) -> bool:
        """Remove a student from a batch."""
        batch = self.get_batch_by_id(batch_id)
        if batch is None:
            return False
        if student_id in batch.enrolled_students:
            batch.enrolled_students.remove(student_id)
            return True
        return False

    def delete_batch(self, batch_id: str) -> bool:
        """Remove a batch by ID."""
        batch = self.get_batch_by_id(batch_id)
        if batch:
            self.batches.remove(batch)
            return True
        return False