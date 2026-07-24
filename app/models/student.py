"""Student domain model."""
from dataclasses import dataclass, field
from datetime import datetime


# ── REFACTORING NOTES ──────────────────────────────────────────────────
# 1. REMOVED `TypedDict` mixin — a class cannot be both a @dataclass and
#    TypedDict simultaneously. Using only @dataclass keeps the model
#    consistent and avoids runtime conflicts.
#
# 2. REMOVED `PIL.Image` import — storing a PIL Image object directly in
#    a data model couples it to PIL. Using a `str` (file path or base64)
#    keeps the model serializable and framework-agnostic.
#
# 3. MOVED required fields BEFORE default fields — Python dataclasses
#    require all non-default fields to come first. The original had
#    `created_at`, `updated_at` (no defaults) after fields that had
#    defaults, which raises a TypeError at runtime.
#
# 4. USED `field(default_factory=lambda: datetime.now().isoformat())`
#    for timestamps — avoids the common mutable-default pitfall and
#    generates a fresh timestamp per instance rather than import-time.
#
# 5. ADDED `full_name` property — avoids repeated f-string concatenation
#    throughout the codebase.
#
# 6. FIXED TYPO: `Educational_background` → `educational_background`
#    for consistent snake_case naming.
# ───────────────────────────────────────────────────────────────────────
@dataclass
class Student:
    """Represents a registered learner in the academy."""
    student_id: str
    first_name: str
    last_name: str
    gender: str
    email: str
    phone: str
    emergency_contact: str
    educational_background: str
    date_of_birth: str
    passport_photograph: str = ""  # file path or base64-encoded image
    status: str = "active"  # active, suspended, graduated
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"