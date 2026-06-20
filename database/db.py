import sqlite3

# =========================================
# DATABASE CONNECTION
# =========================================

conn = sqlite3.connect("resume_data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        username    TEXT,
        filename    TEXT,
        ats_score   REAL,
        job_match   REAL,
        ml_score    REAL,
        category    TEXT,
        skills      TEXT,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# =========================================
# SAVE RESUME DATA
# =========================================

def save_resume_data(username, filename, ats_score, job_match, ml_score, category, skills):
    try:
        cursor.execute("""
            INSERT INTO resumes (username, filename, ats_score, job_match, ml_score, category, skills)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, filename, ats_score, job_match, ml_score, category, skills))
        conn.commit()
        return True
    except Exception as e:
        print(f"DB save error: {e}")
        return False

# =========================================
# GET RESUMES BY USER
# =========================================

def get_user_resumes(username):
    try:
        cursor.execute(
            "SELECT * FROM resumes WHERE username = ? ORDER BY upload_time DESC",
            (username,)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"DB fetch error: {e}")
        return []

# =========================================
# GET ALL RESUMES
# =========================================

def get_all_resumes():
    try:
        cursor.execute("SELECT * FROM resumes ORDER BY upload_time DESC")
        return cursor.fetchall()
    except Exception as e:
        print(f"DB fetch error: {e}")
        return []
