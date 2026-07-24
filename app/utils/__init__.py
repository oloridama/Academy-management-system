"""Utility helpers used across the application."""


def generate_id(prefix: str, counter: int) -> str:
    """Generate a formatted ID string (e.g., 'ST0001', 'INST0003')."""
    return f"{prefix}{counter:04d}"


def parse_full_name(full_name: str) -> tuple[str, str]:
    """Split a full name into (first_name, last_name)."""
    parts = full_name.strip().split(" ", 1)
    first = parts[0] if parts else ""
    last = parts[1] if len(parts) > 1 else ""
    return first, last


def is_valid_status(value: str, allowed: tuple[str, ...]) -> bool:
    """Check if a status string is in the set of allowed values."""
    return value.lower() in {s.lower() for s in allowed}


def format_date(year: int, month: int, day: int) -> str:
    """Format a date as ISO 8601 (YYYY-MM-DD)."""
    return f"{year:04d}-{month:02d}-{day:02d}"
