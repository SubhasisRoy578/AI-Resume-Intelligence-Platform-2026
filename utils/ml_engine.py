"""
ML Engine — TF-IDF vectorization, cosine similarity,
keyword density, skill gap analysis, and section detection.
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# =========================================
# TEXT PREPROCESSING
# =========================================

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s+#.]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# =========================================
# TF-IDF JOB MATCH
# =========================================

def tfidf_job_match(resume_text: str, job_description: str) -> float:
    if not resume_text.strip() or not job_description.strip():
        return 0.0
    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True
        )
        matrix = vectorizer.fit_transform([
            preprocess_text(resume_text),
            preprocess_text(job_description)
        ])
        score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return round(float(score) * 100, 2)
    except Exception as e:
        print(f"[ml] TF-IDF error: {e}")
        return 0.0

# =========================================
# KEYWORD DENSITY
# =========================================

def keyword_density_score(resume_text: str, keywords: list) -> dict:
    if not resume_text or not keywords:
        return {"density_score": 0, "keyword_freq": {}}

    clean = preprocess_text(resume_text)
    keyword_freq = {kw: clean.count(preprocess_text(kw)) for kw in keywords}
    matched = sum(1 for v in keyword_freq.values() if v > 0)
    density_score = round((matched / len(keywords)) * 100, 2)

    # Only keep skills that appear at least once for the chart
    keyword_freq_filtered = {k: v for k, v in keyword_freq.items() if v > 0}

    return {
        "density_score": density_score,
        "keyword_freq": keyword_freq_filtered
    }

# =========================================
# SKILL GAP ANALYSIS
# =========================================

def skill_gap_analysis(detected_skills: list, job_description: str,
                        skills_list: list) -> dict:
    if not job_description.strip():
        return {"missing_skills": [], "gap_score": 0,
                "jd_skills_total": 0, "missing_count": 0}

    jd_clean = preprocess_text(job_description)
    jd_skills = [s for s in skills_list if preprocess_text(s) in jd_clean]
    missing = [s for s in jd_skills if s not in detected_skills]

    gap_score = round((len(missing) / len(jd_skills)) * 100, 2) if jd_skills else 0
    missing_ranked = sorted(
        missing,
        key=lambda s: jd_clean.count(preprocess_text(s)),
        reverse=True
    )

    return {
        "missing_skills": missing_ranked,
        "gap_score": gap_score,
        "jd_skills_total": len(jd_skills),
        "missing_count": len(missing)
    }

# =========================================
# SECTION DETECTOR
# =========================================

SECTION_PATTERNS = {
    "education":    r"\b(education|university|college|degree|b\.?tech|m\.?tech|bsc|msc|bachelor|master|phd)\b",
    "experience":   r"\b(experience|internship|worked at|employment|position|job|role|company)\b",
    "projects":     r"\b(project|built|developed|created|implemented|deployed)\b",
    "skills":       r"\b(skills|technologies|tools|frameworks|languages|proficient)\b",
    "achievements": r"\b(achievement|award|honor|rank|winner|certificate|scholarship)\b",
    "contact":      r"\b(email|phone|linkedin|github|contact|portfolio)\b",
}

def detect_resume_sections(resume_text: str) -> dict:
    text_lower = resume_text.lower()
    sections = {
        name: bool(re.search(pattern, text_lower))
        for name, pattern in SECTION_PATTERNS.items()
    }
    section_score = round(sum(sections.values()) / len(sections) * 100, 2)
    return {"sections": sections, "section_score": section_score}

# =========================================
# SCORE EXPLANATION
# =========================================

def generate_score_explanation(ml_score: float, tfidf_score: float,
                                density_score: float, section_score: float) -> str:
    parts = []
    if tfidf_score >= 70:
        parts.append("strong semantic alignment with the job description")
    elif tfidf_score >= 40:
        parts.append("moderate alignment with the job description")
    else:
        parts.append("low keyword overlap with the job description")

    if density_score >= 70:
        parts.append("good coverage of required skills")
    elif density_score >= 40:
        parts.append("partial coverage of required skills")
    else:
        parts.append("missing several key required skills")

    if section_score >= 80:
        parts.append("well-structured resume sections")
    elif section_score >= 50:
        parts.append("some resume sections need improvement")
    else:
        parts.append("resume structure needs significant work")

    verdict = "Strong" if ml_score >= 70 else ("Moderate" if ml_score >= 45 else "Needs Work")
    return f"{verdict} resume — {', '.join(parts)}."

# =========================================
# MASTER ML SCORE
# =========================================

def compute_ml_resume_score(
    resume_text: str,
    job_description: str,
    detected_skills: list,
    required_skills: list,
    skills_list: list
) -> dict:
    tfidf_score = tfidf_job_match(resume_text, job_description) if job_description.strip() else 50.0
    density_result = keyword_density_score(resume_text, required_skills)
    section_result = detect_resume_sections(resume_text)
    gap_result = skill_gap_analysis(detected_skills, job_description, skills_list)

    ml_score = min(round(
        tfidf_score * 0.40 +
        density_result["density_score"] * 0.30 +
        section_result["section_score"] * 0.30,
        2
    ), 100)

    explanation = generate_score_explanation(
        ml_score, tfidf_score,
        density_result["density_score"],
        section_result["section_score"]
    )

    return {
        "ml_score":      ml_score,
        "tfidf_score":   tfidf_score,
        "density_score": density_result["density_score"],
        "section_score": section_result["section_score"],
        "sections":      section_result["sections"],
        "keyword_freq":  density_result["keyword_freq"],
        "gap_result":    gap_result,
        "explanation":   explanation,
    }
