"""Enrollment domain model."""
from dataclasses import dataclass, field
from datetime import datetime


# ── REFACTORING NOTES ──────────────────────────────────────────────────
# 1. REMOVED dependency on `app.models.date.Date` — the custom Date
#    class added complexity with no benefit over an ISO-format string.
#    Using `str` keeps the model JSON-serializable and easier to persist.
#
# 2. MADE `enrollment_id`, `student_id`, `batch_id` REQUIRED — an
#    enrollment record is meaningless without identifying who is enrolled
#    in what. Original empty-string defaults allowed corrupt records.
#
# 3. CHANGED `payment_status: bool` → `payment_status: str` — a boolean
#    only captures paid/not-paid. Using a string enum ("unpaid", "paid",
#    "refunded") supports real-world payment lifecycles.
#
# 4. RENAMED `status` → `completion_status` — distinguishes enrollment
#    completion (active/suspended/completed/dropped) from payment status,
#    which are two independent concerns.
#
# 5. FIXED `Enrollment_date` (PascalCase) → `enrollment_date` (snake_case)
#    for consistent Python naming conventions.
# ───────────────────────────────────────────────────────────────────────
@dataclass
class Enrollment:
    """Represents a student's enrollment in a specific batch."""
    enrollment_id: str
    student_id: str
    batch_id: str
    enrollment_date: str = field(default_factory=lambda: datetime.now().isoformat())
    payment_status: str = "unpaid"  # unpaid, paid, refunded
    completion_status: str = "active"  # active, suspended, completed, dropped
