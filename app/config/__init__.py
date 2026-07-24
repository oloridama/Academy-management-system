"""Application configuration constants."""

# ── Academy Info ───────────────────────────────────────────────────────
ACADEMY_NAME = "Academy Management System"
ACADEMY_VERSION = "0.1.0"

# ── Database ───────────────────────────────────────────────────────────
DATABASE_PATH = "academy_data.json"

# ── ID Formats ─────────────────────────────────────────────────────────
STUDENT_ID_PREFIX = "ST"
INSTRUCTOR_ID_PREFIX = "INST"
ENROLLMENT_ID_PREFIX = "ENR"
BATCH_ID_PREFIX = "BATCH"
COURSE_ID_PREFIX = "CRS"
REGISTRATION_ID_PREFIX = "REG"

# ── Status Enums ───────────────────────────────────────────────────────
STUDENT_STATUSES = ("active", "suspended", "graduated")
BATCH_STATUSES = ("upcoming", "active", "completed")
ENROLLMENT_PAYMENT_STATUSES = ("unpaid", "paid", "refunded")
ENROLLMENT_COMPLETION_STATUSES = ("active", "suspended", "completed", "dropped")
REGISTRATION_STATUSES = ("pending", "completed", "rejected")
INSTRUCTOR_STATUSES = ("active", "inactive")
