"""
User API endpoints.
Depends on: src/utils.py (validate_email, hash_password)
            src/db.py (get_db, UserRecord)
"""

from src.utils import validate_email, hash_password
from src.db import get_db, UserRecord


def create_user(email: str, password: str) -> dict:
    """Create a new user. Returns user dict or raises ValueError."""
    if not validate_email(email):
        raise ValueError(f"Invalid email: {email}")

    db = get_db()
    if db.find_user(email):
        raise ValueError(f"User already exists: {email}")

    user = UserRecord(
        email=email,
        password_hash=hash_password(password),
    )
    db.insert(user)
    return {"id": user.id, "email": user.email}


def get_user(email: str) -> dict | None:
    """Get user by email. Returns None if not found."""
    db = get_db()
    user = db.find_user(email)
    if not user:
        return None
    return {"id": user.id, "email": user.email}
