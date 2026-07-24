"""Batch domain model."""
from dataclasses import dataclass, field


# ── REFACTORING NOTES ──────────────────────────────────────────────────
# 1. CHANGED `enrolled_students: list[dict[str, str]]` → `list[str]` —
#    storing student IDs (strings) is simpler and sufficient for linking
#    to Student records. The original dict[str,str] format had no
#    consistent key structure and made lookups fragile.
#
# 2. USED `field(default_factory=list)` for both `enrolled_students`
#    and `instructors` — eliminates the classic Python mutable-default
#    bug where `= None` + manual list creation shared state across
#    instances.
#
# 3. MADE `batch_id`, `course_id`, `course_name`, `start_date`,
#    `end_date` REQUIRED (no defaults) — a batch is meaningless without
#    these. The original had empty-string defaults for all, allowing
#    incomplete/invalid Batch objects to be created silently.
#
# 4. ADDED `course_id` — separates the course identity from its display
#    name, enabling proper relational linking.
#
# 5. ADDED `schedule` — captures class timing (e.g. "Mon/Wed 9-11")
#    which is essential for attendance tracking.
# ───────────────────────────────────────────────────────────────────────
@dataclass
class Batch:
    """A scheduled delivery of a course with dates, capacity, and instructors."""
    batch_id: str
    course_id: str
    course_name: str
    start_date: str
    end_date: str
    capacity: int = 0
    enrolled_students: list[str] = field(default_factory=list)  # list of student IDs
    instructors: list[str] = field(default_factory=list)  # list of instructor IDs
    schedule: str = ""  # e.g. "Mon/Wed/Fri 9:00-11:00"
    status: str = "upcoming"  # upcoming, active, completed