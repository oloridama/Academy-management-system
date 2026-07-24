"""Instructor data access layer."""
from app.models.instructor import Instructor


class InstructorRepository:
    """Manages CRUD operations for Instructor entities."""

    # ── REFACTORING NOTES ──────────────────────────────────────────────
    # 1. REMOVED `tutor: type[Instructor]` singleton template — same
    #    anti-pattern as other repositories. Now stores independent
    #    instances in a list.
    #
    # 2. FIXED ID generation — the original used initials + "00" which
    #    would collide after the second instructor with the same initials.
    #    Now uses a counter-based scheme (INST####) with uniqueness
    #    tracking.
    #
    # 3. `add_instructor` now accepts qualification and courses — the
    #    original omitted these fields entirely.
    #
    # 4. FIXED `get_instructor_id` — the original iterated
    #    `range(self.tutors)` (range over a list, TypeError) instead of
    #    `self.tutors` directly.
    #
    # 5. ADDED `get_instructor_by_id`, `update_instructor` — needed by
    #    services for instructor management workflows.
    # ───────────────────────────────────────────────────────────────────

    def __init__(self):
        self.instructors: list[Instructor] = []
        self._id_counter: int = 1

    def add_instructor(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        date_of_birth: str = "",
        qualification: str = "",
        courses: list[str] | None = None,
    ) -> Instructor:
        """Create and store a new instructor profile."""
        instructor_id = self._generate_id()

        instructor = Instructor(
            instructor_id=instructor_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            qualification=qualification,
            courses=courses if courses is not None else [],
        )
        self.instructors.append(instructor)
        return instructor

    def get_instructor_by_id(self, instructor_id: str) -> Instructor | None:
        """Find an instructor by their ID."""
        for instructor in self.instructors:
            if instructor.instructor_id == instructor_id:
                return instructor
        return None

    def get_instructor_by_name(self, first_name: str, last_name: str) -> Instructor | None:
        """Find an instructor by name."""
        for instructor in self.instructors:
            if (
                instructor.first_name.lower() == first_name.lower()
                and instructor.last_name.lower() == last_name.lower()
            ):
                return instructor
        return None

    def get_all_instructors(self) -> list[Instructor]:
        """Return all instructors."""
        return self.instructors

    def update_instructor(self, instructor_id: str, **kwargs) -> Instructor | None:
        """Update an instructor's profile fields."""
        instructor = self.get_instructor_by_id(instructor_id)
        if instructor is None:
            return None
        for key, value in kwargs.items():
            if hasattr(instructor, key):
                setattr(instructor, key, value)
        return instructor

    def deactivate_instructor(self, instructor_id: str) -> bool:
        """Mark an instructor as inactive."""
        instructor = self.get_instructor_by_id(instructor_id)
        if instructor:
            instructor.status = "inactive"
            return True
        return False

    def remove_instructor(self, instructor_id: str) -> bool:
        """Permanently remove an instructor."""
        instructor = self.get_instructor_by_id(instructor_id)
        if instructor:
            self.instructors.remove(instructor)
            return True
        return False

    def _generate_id(self) -> str:
        """Generate a unique instructor ID in the format INST####."""
        while True:
            candidate = f"INST{self._id_counter:04d}"
            self._id_counter += 1
            if not self.get_instructor_by_id(candidate):
                return candidate