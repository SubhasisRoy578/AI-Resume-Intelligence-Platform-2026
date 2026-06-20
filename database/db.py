"""
Resume Database — thread-safe SQLite with per-call connections.
Fixes the global connection bug that caused silent data corruption
in multi-user Streamlit deployments.
"""

import sqlite3
import contextlib
from pathlib import Path

DB_PATH = Path("resume_data.db")

# =========================================
# CONNECTION FACTORY
# =========================================

@contextlib.contextmanager
def get_conn():
    """Always open a fresh connection; close it when done."""
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
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS resumes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT    NOT NULL,
                filename    TEXT    NOT NULL,
                ats_score   REAL    DEFAULT 0,
                job_match   REAL    DEFAULT 0,
                ml_score    REAL    DEFAULT 0,
                category    TEXT    DEFAULT 'General',
                skills      TEXT    DEFAULT '',
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS feedback_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT    NOT NULL,
                feature     TEXT    NOT NULL,
                rating      INTEGER CHECK(rating BETWEEN 1 AND 5),
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

# =========================================
# SAVE RESUME DATA
# =========================================

def save_resume_data(username, filename, ats_score, job_match,
                     ml_score, category, skills):
    try:
        with get_conn() as conn:
            conn.execute("""
                INSERT INTO resumes
                    (username, filename, ats_score, job_match,
                     ml_score, category, skills)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (username, filename, ats_score, job_match,
                  ml_score, category, skills))
        return True
    except Exception as e:
        print(f"[db] save error: {e}")
        return False

# =========================================
# GET USER RESUMES
# =========================================

def get_user_resumes(username):
    try:
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM resumes WHERE username = ? "
                "ORDER BY upload_time DESC",
                (username,)
            ).fetchall()
        return [tuple(r) for r in rows]
    except Exception as e:
        print(f"[db] fetch error: {e}")
        return []

# =========================================
# GLOBAL STATS (for landing page)
# =========================================

def get_global_stats():
    try:
        with get_conn() as conn:
            total = conn.execute(
                "SELECT COUNT(*) FROM resumes"
            ).fetchone()[0]
            avg_ats = conn.execute(
                "SELECT AVG(ats_score) FROM resumes"
            ).fetchone()[0] or 0
            users = conn.execute(
                "SELECT COUNT(DISTINCT username) FROM resumes"
            ).fetchone()[0]
        return {"total": total, "avg_ats": round(avg_ats, 1), "users": users}
    except Exception as e:
        print(f"[db] stats error: {e}")
        return {"total": 0, "avg_ats": 0, "users": 0}

# =========================================
# DELETE USER HISTORY ENTRY
# =========================================

def delete_resume_entry(entry_id: int, username: str) -> bool:
    """Deletes a specific resume entry, scoped to the owner."""
    try:
        with get_conn() as conn:
            conn.execute(
                "DELETE FROM resumes WHERE id = ? AND username = ?",
                (entry_id, username)
            )
        return True
    except Exception as e:
        print(f"[db] delete error: {e}")
        return False

# Run schema init on import
init_db()
