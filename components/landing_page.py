"""
Landing Page — modern hero section with live stats from DB.
"""

import streamlit as st
from database.db import get_global_stats


def show_landing_page():

    stats = get_global_stats()

    # ── Navbar ────────────────────────────────────────────────
    st.markdown("""
    <div class="navbar">
        <div class="nav-logo">⚡ ResumeIQ</div>
        <div class="nav-links">
            <span>Features</span>
            <span>ML Analysis</span>
            <span>AI Tools</span>
            <span>Compare</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Hero ─────────────────────────────────────────────────
    st.markdown(f"""
    <div class="hero-section">
        <div style="display:inline-block;background:rgba(129,140,248,0.12);
                    border:1px solid rgba(129,140,248,0.3);border-radius:50px;
                    padding:6px 20px;font-size:13px;color:#a5b4fc;
                    letter-spacing:1px;text-transform:uppercase;margin-bottom:28px">
            ✦ AI + ML Powered Resume Intelligence
        </div>
        <h1 class="hero-title">
            Know <em>exactly</em> why<br>
            <span class="gradient-text">your resume works</span>
        </h1>
        <p class="hero-subtitle">
            Upload your resume and get ATS scoring, TF-IDF semantic job matching,
            skill gap analysis, AI-generated cover letters, interview prep,
            and a side-by-side version comparator — all in one platform.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats ─────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    def _stat(col, num, label, color="#38bdf8"):
        with col:
            st.markdown(f"""
            <div class="stats-card" style="border-top:2px solid {color}">
                <h2 style="color:{color}">{num}</h2>
                <p>{label}</p>
            </div>
            """, unsafe_allow_html=True)

    _stat(c1, f"{max(stats['total'], 0):,}",
          "Resumes Analysed", "#38bdf8")
    _stat(c2, f"{max(stats['avg_ats'], 0):.0f}%",
          "Avg ATS Score",    "#818cf8")
    _stat(c3, f"{max(stats['users'], 0):,}",
          "Active Users",     "#c084fc")
    _stat(c4, "6",
          "Analysis Dimensions", "#34d399")

    # ── Feature cards ─────────────────────────────────────────
    st.markdown("<h2 class='section-title'>Everything you need to get hired</h2>",
                unsafe_allow_html=True)

    features = [
        ("📊", "ATS Scoring",
         "Rule-based ATS score matching your resume to the required skills for any role."),
        ("🧠", "ML Job Match",
         "TF-IDF vectorization + cosine similarity for real semantic resume-to-JD matching."),
        ("🔍", "Skill Gap Finder",
         "NLP-based detection of skills the JD needs that your resume is missing."),
        ("🤖", "AI Writing Tools",
         "Groq-powered resume summary, feedback, cover letter, and interview Q generation."),
        ("⚖️", "Version Comparator",
         "Upload two versions of your resume and see exactly which changes moved the needle."),
        ("🛣", "Career Roadmap",
         "Personalised career path and milestone roadmap based on your detected skill set."),
    ]

    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for col, (icon, title, desc) in zip(cols, features[i:i+3]):
            with col:
                st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────
    st.markdown("""
    <div class="cta-section">
        <h2>Ready to optimise your resume?</h2>
        <p>Sign up below — it's free. Get your first analysis in under 60 seconds.</p>
    </div>
    """, unsafe_allow_html=True)
