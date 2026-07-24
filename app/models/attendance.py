"""Attendance domain model."""
from dataclasses import dataclass, field


# ── REFACTORING NOTES ──────────────────────────────────────────────────
# 1. RENAMED `Attendance` → `AttendanceRecord` — the original name
#    conflicted with the module name (attendance.py) and was too generic.
#    The new name clearly signals "one person's presence on one day."
#
# 2. FIXED FIELD ORDER — the original had a required `present_status:
#    bool` AFTER optional fields with defaults. Dataclasses require all
#    required fields to come before any field with a default.
#
# 3. CHANGED `date: Date` → `date: str` — removed dependency on the
#    custom Date class. ISO strings are sortable, comparable, and
#    universally supported.
#
# 4. RENAMED `BatchClassAttendance` → `BatchSessionAttendance` —
#    "session" is the ubiquitous term from the project glossary, making
#    the intent clearer.
#
# 5. REPLACED `__post_init__` with `@property` — computed fields
#    (`students_present`, `students_absent`) are now dynamic properties
#    that always stay in sync, rather than being calculated once at
#    init time and becoming stale when lists change.
#
# 6. USED `field(default_factory=list)` — avoids the mutable-default
#    antipattern that the original `= None` + assignment had.
# ───────────────────────────────────────────────────────────────────────
@dataclass
class AttendanceRecord:
    """A single attendance record for a student or instructor on a given date."""
    first_name: str
    last_name: str
    date: str  # ISO date string
    batch_id: str = ""
    is_present: bool = False
    role: str = "student"  # student or instructor


@dataclass
class BatchSessionAttendance:
    """Attendance summary for a single class session within a batch."""
    date: str
    batch_id: str
    lesson_topic: str = ""
    present_student_ids: list[str] = field(default_factory=list)
    present_instructor_ids: list[str] = field(default_factory=list)
    total_enrolled: int = 0

    @property
    def students_present(self) -> int:
        return len(self.present_student_ids)

    @property
    def students_absent(self) -> int:
        return self.total_enrolled - len(self.present_student_ids)