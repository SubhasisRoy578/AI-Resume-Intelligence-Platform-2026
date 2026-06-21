# resume_compare.py
"""
Resume Compare — Side-by-side premium diff of two resume uploads.
Helps users track metric variations and keyword improvements.
"""

import streamlit as st
from utils.parser import extract_resume_text, is_likely_scanned
from utils.skill_engine import (
    detect_skills, detect_job_skills,
    calculate_ats_score, calculate_job_match,
    calculate_resume_strength
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
    """Display premium comparison scorecard with granular before/after tracking"""
    gain = ((val_b - val_a) / val_a * 100) if val_a > 0 else 0.0
    gain_color = "#34d399" if gain >= 0 else "#ef4444"
    gain_sign = "+" if gain >= 0 else ""

    st.markdown(
        f"""
        <div class="card-glass" style="margin: 10px 0; padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="color: var(--text-muted); font-size: 14px; font-weight: 600; letter-spacing: 0.02em;">{label}</span>
                <span style="color: {gain_color}; font-size: 12px; font-weight: 700; background: rgba(255,255,255,0.03); padding: 2px 8px; border-radius: 20px;">
                    {gain_sign}{gain:.1f}% Delta
                </span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 2px; text-transform: uppercase;">Version A</div>
                    <div style="font-size: 22px; font-weight: 700; color: #64748b;">{val_a:.1f}%</div>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="font-size: 28px; font-weight: 800; color: {color};">{val_b:.1f}%</div>
                    <div style="font-size: 11px; color: var(--accent-blue); font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase;">Version B</div>
                </div>
            </div>
            <div style="margin-top: 14px; background: rgba(255,255,255,0.05); border-radius: 10px; height: 6px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, {color}, var(--accent-blue)); height: 100%; width: {min(max(val_b, 0), 100)}%; transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_resume_compare(job_description: str = ""):
    st.markdown("<h2 class='gradient-text'>⚖️ Premium Version Comparator</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:var(--text-muted); margin-bottom: 25px;'>Upload two versions of your resume "
        "side-by-side to track exactly how layout modifications and skill adjustments affect processing ranks.</p>",
        unsafe_allow_html=True
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<h4 style='color:#64748b; margin-bottom: 10px;'>Version A (Baseline Portfolio)</h4>", unsafe_allow_html=True)
        file_a = st.file_uploader("Upload Resume A", type=["pdf"], key="cmp_a", label_visibility="collapsed")
    with col_b:
        st.markdown("<h4 style='color:var(--accent-blue); margin-bottom: 10px;'>Version B (Iterative Profile)</h4>", unsafe_allow_html=True)
        file_b = st.file_uploader("Upload Resume B", type=["pdf"], key="cmp_b", label_visibility="collapsed")

    if not (file_a and file_b):
        st.info("Please provide both configuration versions above to compute delta analytics.")
        return

    with st.spinner("Processing system pipelines and parsing structures..."):
        text_a = extract_resume_text(file_a)
        text_b = extract_resume_text(file_b)

        if is_likely_scanned(text_a) or is_likely_scanned(text_b):
            st.warning("Warning: Flattened layer vectors detected. Text normalization might be partial.")

        def _analyse(text):
            skills = detect_skills(text, SKILLS_LIST)
            jd_skills = detect_job_skills(job_description, SKILLS_LIST)
            ats = calculate_ats_score(skills, REQUIRED_SKILLS)
            match, _ = calculate_job_match(skills, jd_skills)
            strength, _ = calculate_resume_strength(ats, match, skills)
            ml = compute_ml_resume_score(
                text, job_description, skills, REQUIRED_SKILLS, SKILLS_LIST
            )
            return ats, match, strength, ml, skills

        ats_a, match_a, str_a, ml_a, skills_a = _analyse(text_a)
        ats_b, match_b, str_b, ml_b, skills_b = _analyse(text_b)

    st.markdown("<br><h3 style='color:white; font-size:20px; font-weight:700;'>Target Benchmark Metrics</h3>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        _score_card("ATS Optimization Matrix", ats_a, ats_b, "var(--accent-blue)")
    with c2:
        _score_card("Contextual Profile Match", match_a, match_b, "var(--accent-purple)")
    with c3:
        _score_card("Aggregate Strength Metric", str_a, str_b, "#c084fc")

    c4, c5 = st.columns(2)
    with c4:
        _score_card("Vector Space Similarity (TF-IDF)", ml_a.get("tfidf_score", 0.0), ml_b.get("tfidf_score", 0.0), "var(--accent-green)")
    with c5:
        _score_card("Deep-Learning Predictive Score", ml_a.get("ml_score", 0.0), ml_b.get("ml_score", 0.0), "#fb923c")

    # Tracking Keyword Alterations
    st.markdown("<br><h3 style='color:white; font-size:20px; font-weight:700;'>Semantic Structure Mutation</h3>", unsafe_allow_html=True)
    gained = set(skills_b) - set(skills_a)
    lost = set(skills_a) - set(skills_b)

    g_col, l_col = st.columns(2)
    with g_col:
        st.markdown("<h4 style='color:#34d399; margin-bottom:12px;'>✅ Introduced Vectors in Version B</h4>", unsafe_allow_html=True)
        if gained:
            skills_html = "".join([f'<span style="background:rgba(52,211,153,0.1); color:#34d399; border:1px solid rgba(52,211,153,0.2); padding: 4px 10px; border-radius: 6px; display:inline-block; margin: 4px; font-size:13px; font-weight:500;">{s}</span>' for s in sorted(gained)])
            st.markdown(f'<div class="card-glass">{skills_html}</div>', unsafe_allow_html=True)
        else:
            st.caption("No expansion parameters detected.")

    with l_col:
        st.markdown("<h4 style='color:#ef4444; margin-bottom:12px;'>❌ Extracted Vectors from Version B</h4>", unsafe_allow_html=True)
        if lost:
            skills_html = "".join([f'<span style="background:rgba(239,68,68,0.1); color:#ef4444; border:1px solid rgba(239,68,68,0.2); padding: 4px 10px; border-radius: 6px; display:inline-block; margin: 4px; font-size:13px; font-weight:500;">{s}</span>' for s in sorted(lost)])
            st.markdown(f'<div class="card-glass">{skills_html}</div>', unsafe_allow_html=True)
        else:
            st.caption("No compression metrics detected.")
