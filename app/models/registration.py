"""Registration domain model."""
from dataclasses import dataclass, field
from datetime import datetime


# ── REFACTORING NOTES ──────────────────────────────────────────────────
# 1. FLATTENED `prospect_information: dict[str, Student]` into explicit
#    fields (`prospect_first_name`, `prospect_email`, etc.) — a
#    registration captures prospect data BEFORE they become a Student.
#    Embedding a full Student object (with student_id, created_at, etc.)
#    was semantically wrong: the prospect doesn't have these yet.
#
# 2. REMOVED `selected_batch: Batch` — embedding a full Batch object
#    creates tight coupling and duplicates data. Using
#    `selected_batch_id: str` is simpler, serializable, and sufficient.
#
# 3. REMOVED dependency on `app.models.date.Date` — same rationale as
#    Enrollment: ISO string is simpler and more portable.
#
# 4. MADE `registration_id` and `admission_officer` REQUIRED — a
#    registration without an officer or ID is invalid by definition.
#
# 5. CHANGED `payment_status: bool` → `payment_status: str` — same
#    rationale as Enrollment: supports "unpaid"/"paid" lifecycle.
# ───────────────────────────────────────────────────────────────────────
@dataclass
class Registration:
    """Represents the admission process for a prospect becoming a student."""
    registration_id: str
    admission_officer: str
    status: str = "pending"  # pending, completed, rejected
    application_date: str = field(default_factory=lambda: datetime.now().isoformat())
    prospect_first_name: str = ""
    prospect_last_name: str = ""
    prospect_email: str = ""
    prospect_phone: str = ""
    prospect_dob: str = ""
    prospect_gender: str = ""
    prospect_background: str = ""
    selected_batch_id: str = ""
    payment_status: str = "unpaid"  # unpaid, paid
    notes: str = ""