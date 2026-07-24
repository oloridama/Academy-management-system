"""Instructor domain model."""
from dataclasses import dataclass, field


# ── REFACTORING NOTES ──────────────────────────────────────────────────
# 1. REORDERED FIELDS — moved `instructor_id` to the front as a
#    required field. The original had it buried in the middle, but IDs
#    should always come first for readability and consistency with other
#    models.
#
# 2. MADE `date_of_birth`, `qualification`, `courses` OPTIONAL (with
#    defaults) — not every instructor record may have these at creation
#    time (e.g., during quick data entry). The original required them
#    all upfront.
#
# 3. ADDED `status` field — needed to track active vs. inactive
#    instructors (mirrors the "deactivate_instructor" intent already
#    present in InstructorRepository).
#
# 4. USED `field(default_factory=list)` for `courses` — same
#    mutable-default fix as other models.
#
# 5. ADDED `full_name` property — eliminates repeated f-string
#    concatenation.
# ───────────────────────────────────────────────────────────────────────
@dataclass
class Instructor:
    """Represents a teaching staff member at the academy."""
    instructor_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    date_of_birth: str = ""
    qualification: str = ""
    courses: list[str] = field(default_factory=list)  # list of course IDs
    status: str = "active"  # active, inactive

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
