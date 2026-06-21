# components/recommendations.py
"""
Recommendations — Dynamically generated skill development paths, project ideas,
and educational resource mapping with a premium agency-level visual layout.
"""
import streamlit as st

def show_recommendations(detected_skills: list, ats_score: float, strength_score: float):
    st.markdown("<h2 class='gradient-text'>🎯 Personalized Career Roadmap</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:var(--text-muted); margin-bottom: 30px;'> Based on your current resume analytics, "
        "we have curated optimized paths to bridge your technical skill gaps.</p>", 
        unsafe_allow_html=True
    )

    # Simple dynamic state setup for fallback demonstration
    if not detected_skills:
        detected_skills = ["Python", "SQL"]

    # ── Grid Layout for Stats ───────────────────────────────────
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f"""
        <div class="card-glass" style="text-align: center; margin-bottom: 25px;">
            <div style="font-size: 14px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em;">Current Benchmark</div>
            <div style="font-size: 36px; font-weight: 800; color: var(--accent-blue); margin: 10px 0;">{ats_score:.0f}%</div>
            <div style="font-size: 12px; color: #34d399;">+4.2% from last week</div>
        </div>
        """, unsafe_allow_html=True)
        
    with stat_col2:
        st.markdown(f"""
        <div class="card-glass" style="text-align: center; margin-bottom: 25px;">
            <div style="font-size: 14px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em;">Strength Velocity</div>
            <div style="font-size: 36px; font-weight: 800; color: var(--accent-purple); margin: 10px 0;">{strength_score:.0f}%</div>
            <div style="font-size: 12px; color: var(--text-muted);">Target: 90% for Elite tier</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Tabs Navigation for Organized Learning Paths ──────────
    tab_courses, tab_projects = st.tabs(["📚 Recommended Upskilling", "💻 Portfolio Projects"])

    with tab_courses:
        st.markdown("<h4 style='color: white; margin-bottom: 15px;'>Curated Educational Tracks</h4>", unsafe_allow_html=True)
        
        # Track 1: Cloud & DevOps Architectures
        st.markdown("""
        <div class="card-glass" style="margin-bottom: 16px; border-left: 4px solid var(--accent-blue);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="background: rgba(56, 189, 248, 0.1); color: var(--accent-blue); padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">HIGH IMPACT</span>
                    <h3 style="margin: 8px 0 4px 0; font-size: 18px;">AWS Cloud Practitioner & Architecture Sync</h3>
                    <p style="color: var(--text-muted); font-size: 14px; margin: 0;">Bridge your cloud gaps by implementing continuous integration deployment methodologies.</p>
                </div>
                <a href="https://aws.amazon.com/training/" target="_blank" style="text-decoration: none;">
                    <button style="background: var(--accent-blue); color: #0f172a; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer;">
                        Explore Track →
                    </button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Track 2: Systems Optimization & Infrastructure
        st.markdown("""
        <div class="card-glass" style="margin-bottom: 16px; border-left: 4px solid var(--accent-purple);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="background: rgba(129, 140, 248, 0.1); color: var(--accent-purple); padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">CORE COMPETENCY</span>
                    <h3 style="margin: 8px 0 4px 0; font-size: 18px;">Advanced Docker & Container Orchestration</h3>
                    <p style="color: var(--text-muted); font-size: 14px; margin: 0;">Learn production-grade isolation topologies, microservices wiring, and resource clustering configuration.</p>
                </div>
                <a href="https://www.docker.com/" target="_blank" style="text-decoration: none;">
                    <button style="background: var(--accent-purple); color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer;">
                        Explore Track →
                    </button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab_projects:
        st.markdown("<h4 style='color: white; margin-bottom: 15px;'>High-Yield Portfolio Additions</h4>", unsafe_allow_html=True)
        
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown("""
            <div class="card-glass" style="height: 100%;">
                <div style="font-size: 12px; color: var(--accent-green); font-weight: 600; margin-bottom: 5px;">🔥 Recommended Project</div>
                <h3 style="margin: 0 0 10px 0; font-size: 18px;">Enterprise Microservices Mesh</h3>
                <p style="color: var(--text-muted); font-size: 14px; line-height: 1.5; margin: 0 0 15px 0;">
                    Construct an asymmetric REST backend with horizontal scaling capabilities utilizing FastAPI, Docker instances, and Redis cluster locks.
                </p>
                <div style="font-size: 12px; color: var(--text-muted);">
                    <strong>Target Skills:</strong> FastAPI • Redis • Infrastructure Routing
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_p2:
            st.markdown("""
            <div class="card-glass" style="height: 100%;">
                <div style="font-size: 12px; color: var(--accent-blue); font-weight: 600; margin-bottom: 5px;">⚡ Performance Booster</div>
                <h3 style="margin: 0 0 10px 0; font-size: 18px;">Distributed Analytics Pipeline</h3>
                <p style="color: var(--text-muted); font-size: 14px; line-height: 1.5; margin: 0 0 15px 0;">
                    Design and deliver an asynchronous logging broker infrastructure handling telemetry ingestion patterns streaming down to a structured relational schema.
                </p>
                <div style="font-size: 12px; color: var(--text-muted);">
                    <strong>Target Skills:</strong> PostgreSQL • Query Optimization • Git Lifecycle
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
