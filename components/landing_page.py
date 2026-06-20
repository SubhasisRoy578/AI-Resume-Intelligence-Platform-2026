import streamlit as st

# =========================================
# LANDING PAGE
# =========================================

def show_landing_page():

    # =====================================
    # NAVBAR
    # =====================================

    st.markdown(
        """
        <div class="navbar">
            <div class="nav-logo">🚀 AI Resume Intelligence</div>
            <div class="nav-links">
                <span>Features</span>
                <span>Analytics</span>
                <span>AI Tools</span>
                <span>Dashboard</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================
    # HERO SECTION
    # =====================================

    st.markdown(
        """
        <div class="hero-section">
            <h1 class="hero-title">
                Transform Your Resume Into
                <br>
                <span class="gradient-text">AI-Powered Intelligence</span>
            </h1>
            <p class="hero-subtitle">
                Advanced ATS analysis, AI resume optimization,
                recruiter insights, career recommendations,
                and interview preparation — all in one platform.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================
    # STATS
    # =====================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="stats-card">
                <h2>95%</h2>
                <p>ATS Accuracy</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="stats-card">
                <h2>50K+</h2>
                <p>Resumes Analyzed</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="stats-card">
                <h2>AI</h2>
                <p>Powered Insights</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="stats-card">
                <h2>2026</h2>
                <p>Next-Gen Platform</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================
    # FEATURES SECTION
    # =====================================

    st.markdown(
        "<h2 class='section-title'>Platform Features</h2>",
        unsafe_allow_html=True
    )

    feature_col1, feature_col2, feature_col3 = st.columns(3)

    with feature_col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3>ATS Intelligence</h3>
                <p>Advanced resume scoring and job matching analytics.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with feature_col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3>AI Resume Tools</h3>
                <p>AI-generated summaries, cover letters, and feedback.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with feature_col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <h3>Career Insights</h3>
                <p>Project recommendations, career paths, and interview prep.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)
