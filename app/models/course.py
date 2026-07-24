"""Course domain model."""
from dataclasses import dataclass, field


# ── REFACTORING NOTES ──────────────────────────────────────────────────
# 1. ADDED `course_id: str` as a required field — every entity needs a
#    unique identifier for lookups, relationships, and persistence. The
#    original had no ID field at all.
#
# 2. ADDED `description`, `duration_weeks`, `category`, `is_compulsory` —
#    the CourseRepository was already trying to set `.field`, `.duration`,
#    and `.compulsory` on Course objects, but the model didn't define
#    those attributes. This caused AttributeError at runtime.
#
# 3. USED `field(default_factory=list)` for `topics` — Python's mutable
#    default arguments are shared across ALL instances (class-level).
#    Using `default_factory` creates a new list per instance.
# ───────────────────────────────────────────────────────────────────────
@dataclass
class Course:
    """Represents a subject taught at the academy."""
    course_id: str
    name: str
    description: str = ""
    topics: list[str] = field(default_factory=list)
    duration_weeks: int = 0
    category: str = ""
    is_compulsory: bool = False
