"""
Auth Database — PBKDF2-HMAC-SHA256 password hashing,
thread-safe per-call SQLite connections.
"""

import sqlite3
import hashlib
import os
import contextlib
from pathlib import Path

DB_PATH = Path("users.db")

# =========================================
# CONNECTION FACTORY
# =========================================

@contextlib.contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# =========================================
# SCHEMA INIT
# =========================================

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                username   TEXT UNIQUE NOT NULL,
                password   TEXT NOT NULL,
                salt       TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

# =========================================
# PASSWORD HASHING
# =========================================

def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = os.urandom(32).hex()
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000
    ).hex()
    return hashed, salt

# =========================================
# INPUT VALIDATION
# =========================================

def validate_credentials(username: str, password: str):
    username = username.strip()
    if not username:
        return False, "Username cannot be empty."
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(username) > 30:
        return False, "Username must be under 30 characters."
    if not all(c.isalnum() or c in "_-" for c in username):
        return False, "Username can only contain letters, numbers, - and _."
    if not password:
        return False, "Password cannot be empty."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    return True, ""

# =========================================
# REGISTER USER
# =========================================

def register_user(username: str, password: str):
    valid, msg = validate_credentials(username, password)
    if not valid:
        return False, msg
    try:
        hashed, salt = hash_password(password)
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",
                (username.strip(), hashed, salt)
            )
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already taken. Please choose another."
    except Exception as e:
        return False, f"Registration failed: {str(e)}"

# =========================================
# LOGIN USER
# =========================================

def login_user(username: str, password: str):
    valid, msg = validate_credentials(username, password)
    if not valid:
        return False, msg
    try:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT password, salt FROM users WHERE username = ?",
                (username.strip(),)
            ).fetchone()
        if not row:
            return False, "Invalid username or password."
        hashed, _ = hash_password(password, row["salt"])
        if hashed == row["password"]:
            return True, "Login successful!"
        return False, "Invalid username or password."
    except Exception as e:
        return False, f"Login failed: {str(e)}"

# =========================================
# CHANGE PASSWORD
# =========================================

def change_password(username: str, old_password: str, new_password: str):
    ok, msg = login_user(username, old_password)
    if not ok:
        return False, "Current password is incorrect."
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters."
    try:
        hashed, salt = hash_password(new_password)
        with get_conn() as conn:
            conn.execute(
                "UPDATE users SET password=?, salt=? WHERE username=?",
                (hashed, salt, username)
            )
        return True, "Password updated successfully."
    except Exception as e:
        return False, f"Failed to update password: {str(e)}"

# Run schema init on import
init_db()
