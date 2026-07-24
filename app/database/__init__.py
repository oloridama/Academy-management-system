"""Database initialization and session management.

Provides a simple JSON-file-based persistence layer that all repositories
can optionally use. The design keeps storage decoupled from the in-memory
repositories — swap this out for SQLite/PostgreSQL later without touching
business logic.
"""
import json
import os
from dataclasses import asdict, is_dataclass
from typing import Any


class Database:
    """Simple file-based JSON database for persistence."""

    def __init__(self, db_path: str = "academy_data.json"):
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self) -> None:
        """Create the database file if it doesn't exist."""
        if not os.path.exists(self.db_path):
            self._write({})

    def _read(self) -> dict:
        """Read the entire database from disk."""
        with open(self.db_path, "r") as f:
            return json.load(f)

    def _write(self, data: dict) -> None:
        """Write the entire database to disk."""
        with open(self.db_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    # ── Collection-level operations ────────────────────────────────────

    def get_collection(self, name: str) -> list[dict]:
        """Get all records from a named collection."""
        data = self._read()
        return data.get(name, [])

    def save_collection(self, name: str, records: list[dict]) -> None:
        """Save an entire collection to disk."""
        data = self._read()
        data[name] = records
        self._write(data)

    def add_record(self, collection: str, record: dict) -> None:
        """Append a single record to a collection."""
        data = self._read()
        if collection not in data:
            data[collection] = []
        data[collection].append(record)
        self._write(data)

    def update_record(
        self, collection: str, key_field: str, key_value: Any, updates: dict
    ) -> bool:
        """Update a record in a collection identified by a key field."""
        data = self._read()
        records = data.get(collection, [])
        for record in records:
            if record.get(key_field) == key_value:
                record.update(updates)
                self._write(data)
                return True
        return False

    def delete_record(self, collection: str, key_field: str, key_value: Any) -> bool:
        """Delete a record from a collection by key field."""
        data = self._read()
        records = data.get(collection, [])
        for i, record in enumerate(records):
            if record.get(key_field) == key_value:
                records.pop(i)
                self._write(data)
                return True
        return False

    def clear_collection(self, name: str) -> None:
        """Remove all records from a collection."""
        data = self._read()
        data[name] = []
        self._write(data)

    def drop_all(self) -> None:
        """Wipe the entire database."""
        self._write({})


def serialize_dataclass(obj: Any) -> dict:
    """Convert a dataclass instance to a JSON-serializable dict."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    raise TypeError(f"Cannot serialize {type(obj).__name__}")
