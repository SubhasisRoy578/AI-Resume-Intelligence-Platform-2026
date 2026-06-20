"""
ML Engine — Real machine learning for resume analysis.

Uses:
- TF-IDF Vectorization
- Cosine Similarity (job matching)
- Keyword density scoring
- Skill gap analysis
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# =========================================
# TEXT PREPROCESSING
# =========================================

def preprocess_text(text: str) -> str:
    """Clean and normalize text for ML processing."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s+#]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# =========================================
# TF-IDF JOB MATCH SCORE
# =========================================

def tfidf_job_match(resume_text: str, job_description: str) -> float:
    """
    Uses TF-IDF vectorization + cosine similarity to compute
    how closely a resume matches a job description.
    Returns a score from 0 to 100.
    """
    if not resume_text.strip() or not job_description.strip():
        return 0.0

    try:
        resume_clean = preprocess_text(resume_text)
        jd_clean = preprocess_text(job_description)

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),   # unigrams + bigrams
            max_features=5000,
            sublinear_tf=True
        )

        tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

        return round(float(similarity) * 100, 2)

    except Exception as e:
        print(f"TF-IDF error: {e}")
        return 0.0

# =========================================
# KEYWORD DENSITY SCORE
# =========================================

def keyword_density_score(resume_text: str, keywords: list) -> dict:
    """
    Measures how densely important keywords appear in the resume.
    Returns per-keyword frequency and an overall density score.
    """
    if not resume_text or not keywords:
        return {"density_score": 0, "keyword_freq": {}}

    clean = preprocess_text(resume_text)
    words = clean.split()
    total_words = max(len(words), 1)

    keyword_freq = {}
    for kw in keywords:
        kw_clean = preprocess_text(kw)
        count = clean.count(kw_clean)
        keyword_freq[kw] = count

    matched = sum(1 for v in keyword_freq.values() if v > 0)
    density_score = round((matched / len(keywords)) * 100, 2)

    return {
        "density_score": density_score,
        "keyword_freq": keyword_freq
    }

# =========================================
# SKILL GAP ANALYSIS
# =========================================

def skill_gap_analysis(detected_skills: list, job_description: str, skills_list: list) -> dict:
    """
    Identifies skills mentioned in the job description
    that are missing from the resume.
    Returns missing skills ranked by JD importance (TF-IDF weight).
    """
    if not job_description.strip():
        return {"missing_skills": [], "gap_score": 0}

    jd_clean = preprocess_text(job_description)

    jd_skills = [s for s in skills_list if preprocess_text(s) in jd_clean]
    missing = [s for s in jd_skills if s not in detected_skills]

    gap_score = 0
    if jd_skills:
        gap_score = round((len(missing) / len(jd_skills)) * 100, 2)

    # Rank missing skills by how many times they appear in JD
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
# RESUME SECTION DETECTOR
# =========================================

def detect_resume_sections(resume_text: str) -> dict:
    """
    Detects presence of key resume sections using pattern matching.
    Contributes to overall resume quality score.
    """
    text_lower = resume_text.lower()

    sections = {
        "education":    bool(re.search(r"\b(education|university|college|degree|b\.?tech|m\.?tech|bsc|msc)\b", text_lower)),
        "experience":   bool(re.search(r"\b(experience|internship|worked at|employment|position)\b", text_lower)),
        "projects":     bool(re.search(r"\b(project|built|developed|created|implemented)\b", text_lower)),
        "skills":       bool(re.search(r"\b(skills|technologies|tools|frameworks|languages)\b", text_lower)),
        "achievements": bool(re.search(r"\b(achievement|award|honor|rank|winner|certificate)\b", text_lower)),
        "contact":      bool(re.search(r"\b(email|phone|linkedin|github|contact)\b", text_lower)),
    }

    section_score = round(sum(sections.values()) / len(sections) * 100, 2)

    return {
        "sections": sections,
        "section_score": section_score
    }

# =========================================
# COMBINED ML RESUME SCORE
# =========================================

def compute_ml_resume_score(
    resume_text: str,
    job_description: str,
    detected_skills: list,
    required_skills: list,
    skills_list: list
) -> dict:
    """
    Master function that combines all ML signals into one score.
    """
    # TF-IDF similarity
    tfidf_score = tfidf_job_match(resume_text, job_description) if job_description.strip() else 50.0

    # Keyword density
    density_result = keyword_density_score(resume_text, required_skills)

    # Section quality
    section_result = detect_resume_sections(resume_text)

    # Skill gap
    gap_result = skill_gap_analysis(detected_skills, job_description, skills_list)

    # Weighted final ML score
    ml_score = round(
        tfidf_score      * 0.40 +
        density_result["density_score"] * 0.30 +
        section_result["section_score"] * 0.30,
        2
    )
    ml_score = min(ml_score, 100)

    return {
        "ml_score":       ml_score,
        "tfidf_score":    tfidf_score,
        "density_score":  density_result["density_score"],
        "section_score":  section_result["section_score"],
        "sections":       section_result["sections"],
        "keyword_freq":   density_result["keyword_freq"],
        "gap_result":     gap_result
    }
