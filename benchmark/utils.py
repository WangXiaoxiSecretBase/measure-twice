"""
Utility functions.
NOTE: hash_password uses SHA-256 + salt (NOT bcrypt).
      If you add rate limiting, import RATE_LIMIT_WINDOW from here too.
"""

import hashlib
import re
import os
import time

RATE_LIMIT_WINDOW = 60       # seconds
RATE_LIMIT_MAX_ATTEMPTS = 5  # per window
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

_rate_buckets: dict[str, list[float]] = {}


def validate_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))


def hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    h = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}:{h}"


def check_password(password: str, stored_hash: str) -> bool:
    salt, h = stored_hash.split(":", 1)
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest() == h


def is_rate_limited(key: str) -> bool:
    """Return True if key has exceeded RATE_LIMIT_MAX_ATTEMPTS in RATE_LIMIT_WINDOW."""
    now = time.time()
    bucket = _rate_buckets.get(key, [])
    bucket = [t for t in bucket if now - t < RATE_LIMIT_WINDOW]
    bucket.append(now)
    _rate_buckets[key] = bucket
    return len(bucket) > RATE_LIMIT_MAX_ATTEMPTS
