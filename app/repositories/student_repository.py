"""Student data access layer."""
import random
from app.models.student import Student


class StudentRepository:
    """Manages CRUD operations for Student entities."""

    # ── REFACTORING NOTES ──────────────────────────────────────────────
    # 1. REMOVED `student: type[Student]` parameter — the original took
    #    a class reference and mutated it as a singleton template. This
    #    caused all students to overwrite the same object. Now we store
    #    a list of independent Student instances.
    #
    # 2. CHANGED `self.students_id` (dict) → `self._used_ids` (set) —
    #    a set is the right data structure for "already-used" tracking;
    #    O(1) lookup with no unused values.
    #
    # 3. `add_student` now returns a Student dataclass instance instead
    #    of a plain dict — consistent typing throughout the codebase.
    #
    # 4. FIXED `find_student` — the original tried to read
    #    `self.students_id[id]` where `id` was never assigned, causing
    #    NameError. Now uses proper iteration over Student objects.
    #
    # 5. FIXED `update_student` — the original had `return student`
    #    INSIDE the for-loop, so it always returned after the first
    #    iteration (even if no match).
    #
    # 6. FIXED `deactivate_student` — the original used attribute access
    #    (`student.last_name`) on dict items. Now uses Student dataclass
    #    attributes consistently.
    # ───────────────────────────────────────────────────────────────────

    def __init__(self):
        self.students: list[Student] = []
        self._used_ids: set[str] = set()

    def add_student(
        self,
        firstname: str,
        lastname: str,
        gender: str,
        dob: str,
        email: str,
        phone: str,
        background: str,
        passport: str = "",
        emergency: str = "",
    ) -> Student:
        """Create a new student profile and add it to the repository."""
        student_id = self._generate_id()

        student = Student(
            student_id=student_id,
            first_name=firstname,
            last_name=lastname,
            gender=gender,
            email=email,
            phone=phone,
            emergency_contact=emergency,
            educational_background=background,
            date_of_birth=dob,
            passport_photograph=passport,
        )

        self.students.append(student)
        return student

    def get_student_by_id(self, student_id: str) -> Student | None:
        """Find a student by their ID."""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def find_student(self, firstname: str, lastname: str, student_id: str = "") -> Student | None:
        """Find a student by name and optionally by ID."""
        for student in self.students:
            name_match = (
                student.first_name.lower() == firstname.lower()
                and student.last_name.lower() == lastname.lower()
            )
            if student_id:
                if name_match and student.student_id == student_id:
                    return student
            elif name_match:
                return student
        return None

    def get_all_students(self) -> list[Student]:
        """Return all registered students."""
        return self.students

    def update_student(self, student_id: str, **kwargs) -> Student | None:
        """Update a student's profile fields. Returns the updated student or None."""
        student = self.get_student_by_id(student_id)
        if student is None:
            return None

        for key, value in kwargs.items():
            if hasattr(student, key):
                setattr(student, key, value)
        return student

    def deactivate_student(self, student_id: str) -> bool:
        """Mark a student as inactive (suspended) by ID."""
        student = self.get_student_by_id(student_id)
        if student:
            student.status = "suspended"
            return True
        return False

    def remove_student(self, student_id: str) -> bool:
        """Permanently remove a student from the repository."""
        student = self.get_student_by_id(student_id)
        if student:
            self.students.remove(student)
            self._used_ids.discard(student_id)
            return True
        return False

    def _generate_id(self) -> str:
        """Generate a unique student ID in the format ST####."""
        while True:
            num = random.randint(0, 9999)
            candidate = f"ST{num:04d}"
            if candidate not in self._used_ids:
                self._used_ids.add(candidate)
                return candidate
