"""
Resume Compare — side-by-side diff of two resume uploads.
Helps users see whether changes actually improved their scores.
"""

import streamlit as st
from utils.parser import extract_resume_text, is_likely_scanned
from utils.skill_engine import (
    detect_skills, detect_job_skills,
    calculate_ats_score, calculate_job_match,
    calculate_resume_strength, detect_resume_category
)
from utils.ml_engine import compute_ml_resume_score


SKILLS_LIST = [
    "Python", "Java", "C", "C++", "JavaScript", "TypeScript", "SQL",
    "HTML", "CSS", "React", "Node.js", "Django", "Flask", "FastAPI",
    "Machine Learning", "Deep Learning", "Artificial Intelligence",
    "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "OpenCV",
    "Data Science", "Pandas", "NumPy", "Matplotlib", "Seaborn",
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD",
    "Git", "GitHub", "REST API", "GraphQL",
    "OOP", "DBMS", "Data Structures", "Algorithms",
    "NLP", "Computer Vision", "Generative AI", "LLM",
    "Spring", "Microservices", "Kotlin", "Swift",
    "PostgreSQL", "MongoDB", "Redis", "Elasticsearch",
    "Linux", "Bash", "Terraform", "Ansible",
]

REQUIRED_SKILLS = ["Python", "SQL", "Machine Learning", "Git", "React", "JavaScript"]


def _score_card(label: str, val_a: float, val_b: float, color: str):
    """Display comparison score card with before/after values"""
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
                    border-radius:12px;padding:20px;margin:10px 0;backdrop-filter:blur(10px);">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <span style="color:#94a3b8;font-size:14px;font-weight:500;">{label}</span>
                <span style="color:#64748b;font-size:12px;">⬆ Improvement</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:12px;color:#64748b;margin-bottom:4px;">Version A</div>
                    <div style="font-size:24px;font-weight:700;color:#94a3b8;">{val_a:.1f}%</div>
                </div>
                <div style="text-align:center;flex:1;">
                    <div style="font-size:28px;font-weight:800;color:{color};">{val_b:.1f}%</div>
                    <div style="font-size:12px;color:#38bdf8;">Version B</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:12px;color:#64748b;margin-bottom:4px;">Gain</div>
                    <div style="font-size:20px;font-weight:700;color:#4ade80;">
                        +{((val_b - val_a) / val_a * 100) if val_a > 0 else 0:.1f}%
                    </div>
                </div>
            </div>
            <div style="margin-top:12px;background:rgba(255,255,255,0.05);border-radius:6px;height:6px;overflow:hidden;">
                <div style="background:linear-gradient(90deg, {color}, #38bdf8);height:100%;width:{min(val_b, 100)}%;transition:width 0.5s;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def show_resume_compare(job_description: str = ""):
    st.markdown("<h2 style='color:white'>⚖️ Resume Version Comparator</h2>",
                unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#94a3b8'>Upload two versions of your resume to see "
        "exactly which changes improved your scores.</p>",
        unsafe_allow_html=True
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<h4 style='color:#64748b'>Version A (Original)</h4>",
                    unsafe_allow_html=True)
        file_a = st.file_uploader("Upload Resume A", type=["pdf"], key="cmp_a")
    with col_b:
        st.markdown("<h4 style='color:#38bdf8'>Version B (Updated)</h4>",
                    unsafe_allow_html=True)
        file_b = st.file_uploader("Upload Resume B", type=["pdf"], key="cmp_b")

    if not (file_a and file_b):
        st.info("Upload both versions to see the comparison.")
        return

    with st.spinner("Analysing both versions..."):
        text_a = extract_resume_text(file_a)
        text_b = extract_resume_text(file_b)

        if is_likely_scanned(text_a) or is_likely_scanned(text_b):
            st.warning("One or both PDFs appear to be scanned images. "
                       "Text extraction may be incomplete.")

        def _analyse(text):
            skills = detect_skills(text, SKILLS_LIST)
            jd_skills = detect_job_skills(job_description, SKILLS_LIST)
            ats = calculate_ats_score(skills, REQUIRED_SKILLS)
            match, _ = calculate_job_match(skills, jd_skills)
            strength, bonus = calculate_resume_strength(ats, match, skills)
            ml = compute_ml_resume_score(
                text, job_description, skills, REQUIRED_SKILLS, SKILLS_LIST
            )
            return ats, match, strength, ml, skills

        ats_a, match_a, str_a, ml_a, skills_a = _analyse(text_a)
        ats_b, match_b, str_b, ml_b, skills_b = _analyse(text_b)

    st.markdown("---")
    st.markdown("<h3 style='color:white'>Score Comparison</h3>",
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        _score_card("ATS Score",      ats_a,            ats_b,            "#38bdf8")
    with c2:
        _score_card("Job Match",      match_a,          match_b,          "#818cf8")
    with c3:
        _score_card("Overall Strength", str_a,          str_b,            "#c084fc")

    c4, c5 = st.columns(2)
    with c4:
        _score_card("TF-IDF Match",   ml_a["tfidf_score"],   ml_b["tfidf_score"],   "#34d399")
    with c5:
        _score_card("ML Score",       ml_a["ml_score"],      ml_b["ml_score"],       "#fb923c")

    # Skills gained / lost
    st.markdown("---")
    st.markdown("<h3 style='color:white'>Skill Changes</h3>", unsafe_allow_html=True)
    gained = set(skills_b) - set(skills_a)
    lost   = set(skills_a) - set(skills_b)

    g_col, l_col = st.columns(2)
    with g_col:
        st.markdown("<h4 style='color:#22c55e'>✅ Skills Added in B</h4>",
                    unsafe_allow_html=True)
        if gained:
            for s in sorted(gained):
                st.success(s)
        else:
            st.caption("No new skills detected.")

    with l_col:
        st.markdown("<h4 style='color:#ef4444'>❌ Skills Removed in B</h4>",
                    unsafe_allow_html=True)
        if lost:
            for s in sorted(lost):
                st.error(s)
        else:
            st.caption("No skills removed.")
