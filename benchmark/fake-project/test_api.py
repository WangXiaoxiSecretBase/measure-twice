"""
Tests for src/api.py
Uses src/db.reset_db() to isolate tests.
"""

import pytest
from src.api import create_user, get_user
from src.db import reset_db


@pytest.fixture(autouse=True)
def clean_db():
    reset_db()
    yield
    reset_db()


def test_create_user_success():
    user = create_user("alice@example.com", "password123")
    assert user["email"] == "alice@example.com"
    assert "id" in user


def test_create_user_invalid_email():
    with pytest.raises(ValueError, match="Invalid email"):
        create_user("not-an-email", "password123")


def test_create_user_duplicate():
    create_user("alice@example.com", "password123")
    with pytest.raises(ValueError, match="already exists"):
        create_user("alice@example.com", "other")


def test_get_user_found():
    create_user("bob@example.com", "pw")
    user = get_user("bob@example.com")
    assert user is not None
    assert user["email"] == "bob@example.com"


def test_get_user_not_found():
    assert get_user("nobody@example.com") is None
