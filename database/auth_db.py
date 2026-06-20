import sqlite3
import hashlib
import os

# =========================================
# DATABASE CONNECTION
# =========================================

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        salt     TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

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
        cursor.execute(
            "INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",
            (username.strip(), hashed, salt)
        )
        conn.commit()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists. Please choose another."
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
        cursor.execute(
            "SELECT password, salt FROM users WHERE username = ?",
            (username.strip(),)
        )
        row = cursor.fetchone()
        if not row:
            return False, "Invalid username or password."
        stored_hash, salt = row
        hashed, _ = hash_password(password, salt)
        if hashed == stored_hash:
            return True, "Login successful!"
        return False, "Invalid username or password."
    except Exception as e:
        return False, f"Login failed: {str(e)}"
