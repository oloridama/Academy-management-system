"""Course data access layer."""
from app.models.course import Course


class CourseRepository:
    """Manages CRUD operations for Course entities."""

    # ── REFACTORING NOTES ──────────────────────────────────────────────
    # 1. REMOVED `course: type[Course]` singleton template — same
    #    anti-pattern as the original StudentRepository. Now stores a
    #    list of independent Course instances.
    #
    # 2. `add_course` now creates a Course dataclass instance matching
    #    the actual Course model fields (`course_id`, `name`, `topics`,
    #    `duration_weeks`, `category`, `is_compulsory`). The original
    #    tried to set `.field`, `.duration`, `.compulsory` which didn't
    #    exist, causing AttributeError.
    #
    # 3. ADDED `get_course_by_id`, `get_all_courses`, `update_course` —
    #    the original only had add and delete, with no retrieval methods.
    #
    # 4. `delete_course` is now ID-based, not a nested category search.
    # ───────────────────────────────────────────────────────────────────

    def __init__(self):
        self.courses: list[Course] = []

    def add_course(
        self,
        course_id: str,
        name: str,
        description: str = "",
        topics: list[str] | None = None,
        duration_weeks: int = 0,
        category: str = "",
        is_compulsory: bool = False,
    ) -> Course:
        """Create and store a new course."""
        course = Course(
            course_id=course_id,
            name=name,
            description=description,
            topics=topics if topics is not None else [],
            duration_weeks=duration_weeks,
            category=category,
            is_compulsory=is_compulsory,
        )
        self.courses.append(course)
        return course

    def get_course_by_id(self, course_id: str) -> Course | None:
        """Find a course by its ID."""
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None

    def get_all_courses(self) -> list[Course]:
        """Return all courses."""
        return self.courses

    def get_courses_by_category(self, category: str) -> list[Course]:
        """Return all courses in a given category."""
        return [c for c in self.courses if c.category.lower() == category.lower()]

    def update_course(self, course_id: str, **kwargs) -> Course | None:
        """Update a course's fields."""
        course = self.get_course_by_id(course_id)
        if course is None:
            return None
        for key, value in kwargs.items():
            if hasattr(course, key):
                setattr(course, key, value)
        return course

    def delete_course(self, course_id: str) -> bool:
        """Remove a course by its ID."""
        course = self.get_course_by_id(course_id)
        if course:
            self.courses.remove(course)
            return True
        return False