import streamlit as st

# =========================================
# PAGE CONFIG — must be FIRST
# =========================================

st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    page_icon="🚀",
    layout="wide"
)

# =========================================
# IMPORTS
# =========================================

from utils.parser import extract_resume_text
from utils.skill_engine import (
    detect_skills, detect_job_skills,
    calculate_ats_score, calculate_job_match,
    calculate_resume_strength, detect_resume_category
)
from utils.ml_engine import compute_ml_resume_score

from components.dashboard import show_dashboard
from components.ai_features import show_ai_features
from components.recommendations import show_recommendations
from components.landing_page import show_landing_page
from components.auth_ui import show_auth_ui
from components.ml_dashboard import show_ml_dashboard

from database.db import save_resume_data, get_user_resumes
from resume_compare import show_resume_compare

# =========================================
# API KEY — now using Groq
# =========================================

# Safe retrieval of Groq API Key to prevent app crash when not configured
groq_api_key = st.secrets.get("GROQ_API_KEY", "")

# =========================================
# LOAD CSS
# =========================================

def load_css():
    try:
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("styles.css not found.")

load_css()

# =========================================
# SESSION STATE
# =========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# =========================================
# SKILLS DATABASE
# =========================================

skills_list = [
    "Python", "Java", "C", "C++", "JavaScript", "TypeScript", "SQL",
    "HTML", "CSS", "React", "Node.js", "Django", "Flask", "FastAPI",
    "Machine Learning", "Deep Learning", "Artificial Intelligence",
    "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "OpenCV",
    "Data Science", "Pandas", "NumPy", "Matplotlib", "Seaborn",
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD",
    "Git", "GitHub", "REST API", "GraphQL",
    "OOP", "DBMS", "Data Structures", "Algorithms",
    "NLP", "Computer Vision", "Generative AI", "LLM"
]

required_skills = ["Python", "SQL", "Machine Learning", "Git", "React", "JavaScript"]

# =========================================
# MAIN APP
# =========================================

if st.session_state.logged_in:

    # =====================================
    # SIDEBAR
    # =====================================

    with st.sidebar:
        st.markdown(
            f"<div class='sidebar-welcome'>👋 <b>{st.session_state.username}</b></div>",
            unsafe_allow_html=True
        )
        st.markdown("---")
        
        # Navigation Menu
        app_mode = st.radio(
            "📍 Navigation",
            ["🔍 Single Resume Analyzer", "⚖️ Resume Comparator"],
            key="app_mode"
        )
        
        st.markdown("---")
        st.markdown("<p style='color:#94a3b8;font-size:13px'>AI Resume Intelligence Platform</p>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    # =====================================
    # HEADER
    # =====================================

    st.markdown(
        """
        <h1 class='main-title'>AI Resume Intelligence Platform</h1>
        <p class='dashboard-subtitle'>Upload your resume · Get AI + ML powered insights · Land your dream job</p>
        """,
        unsafe_allow_html=True
    )

    if app_mode == "🔍 Single Resume Analyzer":

        # =====================================
        # UPLOAD + JD
        # =====================================

        col_upload, col_jd = st.columns([1, 1])

        with col_upload:
            uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

        with col_jd:
            job_description = st.text_area(
                "💼 Paste Job Description (optional but recommended)",
                height=150,
                placeholder="Paste the job description here for accurate ML job match and skill gap analysis...",
                key="single_jd"
            )

        # =====================================
        # PROCESS
        # =====================================

        if uploaded_file is not None:

            with st.spinner("🔍 Analyzing your resume with AI + ML..."):

                text = extract_resume_text(uploaded_file)

                if not text.strip():
                    st.error("Could not extract text from this PDF. Please ensure it is not a scanned image.")
                    st.stop()

                resume_text_lower = text.lower()
                jd_text_lower = job_description.lower()

                detected_skills = detect_skills(resume_text_lower, skills_list)
                job_skills = detect_job_skills(jd_text_lower, skills_list)
                ats_score = calculate_ats_score(detected_skills, required_skills)
                job_match_score, matched_skills = calculate_job_match(detected_skills, job_skills)
                strength_score, skill_bonus = calculate_resume_strength(ats_score, job_match_score, detected_skills)
                resume_category = detect_resume_category(resume_text_lower)

                ml_results = compute_ml_resume_score(
                    text, job_description, detected_skills, required_skills, skills_list
                )

                save_resume_data(
                    st.session_state.username,
                    uploaded_file.name,
                    ats_score,
                    job_match_score,
                    ml_results["ml_score"],
                    resume_category,
                    ", ".join(detected_skills)
                )

            st.success(f"✅ Analysis complete for **{uploaded_file.name}**")

            # =====================================
            # TABS
            # =====================================

            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Dashboard",
                "🧠 ML Analysis",
                "🤖 AI Features",
                "🚀 Recommendations",
                "📂 History"
            ])

            with tab1:
                show_dashboard(
                    text, detected_skills, ats_score,
                    job_match_score, strength_score,
                    skill_bonus, resume_category, required_skills
                )

            with tab2:
                show_ml_dashboard(ml_results, detected_skills, job_description)

            with tab3:
                show_ai_features(groq_api_key, text)

            with tab4:
                show_recommendations(detected_skills, ats_score, strength_score)

            with tab5:
                st.markdown("<h3 style='color:white'>📂 Your Resume History</h3>", unsafe_allow_html=True)
                resumes = get_user_resumes(st.session_state.username)
                if resumes:
                    for r in resumes:
                        st.markdown(
                            f"""
                            <div class='glass-card'>
                                <h4>📄 {r[2]}</h4>
                                <span style='color:#38bdf8'><b>ATS:</b> {r[3]:.1f}%</span> &nbsp;
                                <span style='color:#818cf8'><b>Job Match:</b> {r[4]:.1f}%</span> &nbsp;
                                <span style='color:#c084fc'><b>ML Score:</b> {r[5]:.1f}%</span> &nbsp;
                                <span style='color:#94a3b8'><b>Category:</b> {r[6]}</span>
                                <br><small style='color:#64748b'>{r[8]} &nbsp;|&nbsp; Skills: {r[7][:80]}...</small>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No resume history yet.")

        else:
            st.markdown(
                """
                <div class="upload-prompt">
                    <div class="upload-icon">📄</div>
                    <h3>Upload your resume to get started</h3>
                    <p>PDF format supported · AI + ML powered analysis · Results in seconds</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        # =====================================
        # COMPARATOR MODE
        # =====================================
        col_comp_jd, _ = st.columns([2, 1])
        with col_comp_jd:
            compare_jd = st.text_area(
                "💼 Paste Job Description (optional but recommended for matching)",
                height=120,
                placeholder="Paste the job description here for matching both resumes against the job...",
                key="compare_jd"
            )
        show_resume_compare(compare_jd)

# =========================================
# LANDING + AUTH
# =========================================

else:
    show_landing_page()
    show_auth_ui()

# =========================================
# FOOTER
# =========================================

st.markdown("---")
st.markdown(
    """
    <center style='color:#475569;font-size:13px;padding:10px 0'>
        🚀 AI Resume Intelligence Platform &nbsp;·&nbsp;
        Built with Python · Streamlit · Groq AI · scikit-learn · TF-IDF · SQLite
        <br><br>Developed by Subhasis Roy
    </center>
    """,
    unsafe_allow_html=True
)
