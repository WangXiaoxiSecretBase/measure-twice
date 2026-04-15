"""
Database layer.
Uses a simple in-memory store for testing.
UserRecord.id is auto-assigned (incrementing int).
"""

import uuid
from dataclasses import dataclass, field


@dataclass
class UserRecord:
    email: str
    password_hash: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    active: bool = True


class _DB:
    def __init__(self):
        self._users: dict[str, UserRecord] = {}  # keyed by email

    def find_user(self, email: str) -> UserRecord | None:
        return self._users.get(email)

    def insert(self, user: UserRecord) -> None:
        if user.email in self._users:
            raise RuntimeError(f"Duplicate email: {user.email}")
        self._users[user.email] = user

    def delete(self, email: str) -> bool:
        if email not in self._users:
            return False
        del self._users[email]
        return True


_instance: _DB | None = None


def get_db() -> _DB:
    global _instance
    if _instance is None:
        _instance = _DB()
    return _instance


def reset_db() -> None:
    """Call this in tests to get a clean database."""
    global _instance
    _instance = None
