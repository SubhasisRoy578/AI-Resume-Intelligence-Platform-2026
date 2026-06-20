"""
Skill Engine — rule-based ATS scoring, job match,
resume strength, and category detection.
"""

# =========================================
# DETECT SKILLS
# =========================================

def detect_skills(resume_text: str, skills_list: list) -> list:
    """Case-insensitive substring match for each skill."""
    return list({
        skill for skill in skills_list
        if skill.lower() in resume_text.lower()
    })


def detect_job_skills(job_description: str, skills_list: list) -> list:
    """Extract skills mentioned in a job description."""
    return list({
        skill for skill in skills_list
        if skill.lower() in job_description.lower()
    })

# =========================================
# ATS SCORE
# =========================================

def calculate_ats_score(detected_skills: list, required_skills: list) -> float:
    """Percentage of required skills found in the resume."""
    if not required_skills:
        return 0.0
    matched = sum(1 for s in required_skills if s in detected_skills)
    return round((matched / len(required_skills)) * 100, 2)

# =========================================
# JOB MATCH SCORE
# =========================================

def calculate_job_match(detected_skills: list, job_skills: list):
    """Percentage of JD skills the resume covers."""
    if not job_skills:
        return 0.0, []
    matched = [s for s in job_skills if s in detected_skills]
    score = round((len(matched) / len(job_skills)) * 100, 2)
    return score, matched

# =========================================
# RESUME STRENGTH
# =========================================

def calculate_resume_strength(ats_score: float, job_match_score: float,
                               detected_skills: list):
    """
    Weighted composite:
      40% ATS  +  40% Job Match  +  20% skill breadth bonus
    """
    skill_bonus = min(len(detected_skills) * 2, 20)
    raw = ats_score * 0.4 + job_match_score * 0.4 + skill_bonus
    return min(round(raw), 100), skill_bonus

# =========================================
# RESUME CATEGORY
# =========================================

CATEGORY_MAP = [
    (["machine learning", "deep learning", "tensorflow", "pytorch", "keras"],
     "AI / ML Engineer"),
    (["data science", "pandas", "numpy", "matplotlib", "seaborn"],
     "Data Scientist"),
    (["react", "javascript", "typescript", "node.js", "html", "css"],
     "Web Developer"),
    (["aws", "azure", "gcp", "docker", "kubernetes", "ci/cd"],
     "Cloud / DevOps Engineer"),
    (["nlp", "computer vision", "generative ai", "llm"],
     "AI Research Engineer"),
    (["java", "spring", "microservices", "rest api"],
     "Backend Developer"),
]

def detect_resume_category(resume_text: str) -> str:
    text = resume_text.lower()
    best_cat, best_count = "General Resume", 0
    for keywords, label in CATEGORY_MAP:
        count = sum(1 for kw in keywords if kw in text)
        if count > best_count:
            best_count, best_cat = count, label
    return best_cat

# =========================================
# SCORE BADGE LABEL
# =========================================

def score_label(score: float) -> str:
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Fair"
    return "Needs Work"
