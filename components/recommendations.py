# components/recommendations.py
"""
SaaS Skill Gap & Recommendations Engine — 100% Dynamic Upskilling Tracks.
Generates tailored structural roadmaps, courses, and interactive portfolio project targets
exclusively using parsed token data found within the uploaded document.
"""
import streamlit as st

def show_recommendations(detected_skills: list, ats_score: float, strength_score: float):
    st.markdown("<h2 class='gradient-text'>🎯 Personalized Career Roadmap</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:var(--text-muted); margin-bottom: 30px;'>Dynamically generated upskilling "
        "tracks mapping structural vacancies discovered inside your parsed text matrix nodes.</p>", 
        unsafe_allow_html=True
    )

    # ── EMPTY STATE GATEKEEPER (Strict Validation Matrix) ──
    if not st.session_state.get("active_resume_text"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="card-glass" style="text-align: center; padding: 60px 20px; border: 1px dashed rgba(129, 140, 248, 0.3);">
                <div style="font-size: 48px; margin-bottom: 20px;">🛣️</div>
                <h3 style="margin: 0 0 10px 0; color: white;">Upskilling Vector Uninitialized</h3>
                <p style="color: var(--text-muted); max-width: 500px; margin: 0 auto 24px; font-size: 14px;">
                    We cannot formulate automated learning presets without text entities. Run the <strong>Deep Ingestion AI</strong> parsing pass to discover missing nodes.
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        return

    # ── METRIC VARIATION SUMMARY CARDS ──
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f"""
        <div class="card-glass" style="text-align: center; margin-bottom: 25px;">
            <div style="font-size: 13px; color: var(--text-muted); text-transform: uppercase; font-weight: 600;">Ingested Target Benchmark</div>
            <div style="font-size: 36px; font-weight: 800; color: var(--accent-blue); margin: 10px 0;">{ats_score:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
    with stat_col2:
        st.markdown(f"""
        <div class="card-glass" style="text-align: center; margin-bottom: 25px;">
            <div style="font-size: 13px; color: var(--text-muted); text-transform: uppercase; font-weight: 600;">Computed Structural Strength</div>
            <div style="font-size: 36px; font-weight: 800; color: var(--accent-purple); margin: 10px 0;">{strength_score:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Determine missing ecosystem dimensions based explicitly on what tokens DO NOT exist
    skills_set = {s.lower() for s in detected_skills}
    
    # Structural Gap Mapping Logic
    gap_recommendations = []
    
    if "python" not in skills_set and "javascript" not in skills_set:
        gap_recommendations.append({
            "title": "Core Multi-Paradigm Development & Syntax Architectures",
            "desc": "Incorporate production-grade software constructs (Python/TypeScript async patterns) into your application layer descriptions.",
            "link": "https://www.python.org/",
            "type": "CORE COMPETENCY",
            "color": "var(--accent-blue)"
        })
    if "aws" not in skills_set and "docker" not in skills_set:
        gap_recommendations.append({
            "title": "Cloud Orchestration, Containment, & Scalable Infrastructures",
            "desc": "Your profile lacks visible cloud configuration tokens. Integrate Amazon Web Services provisioning, container mapping, and microservice meshes.",
            "link": "https://aws.amazon.com/",
            "type": "HIGH IMPACT",
            "color": "var(--accent-purple)"
        })
    if "machine learning" not in skills_set and "deep learning" not in skills_set:
        gap_recommendations.append({
            "title": "Advanced Data Math Models & Vector Analytics Pipelines",
            "desc": "Bridge the algorithmic logic divide by creating deep engineering layers using statistical predictive tooling arrays.",
            "link": "https://scikit-learn.org/",
            "type": "ELEVATED SPECIALIZATION",
            "color": "var(--accent-green)"
        })

    # Catch-all if user already has an elite profile containing all vocab tokens
    if not gap_recommendations:
        gap_recommendations.append({
            "title": "Distributed Systems Fine-Tuning & High-Performance Edge Computing",
            "desc": "Your technical keyword layout is highly exceptional. Focus on performance profiling, custom tokenization architectures, and lower-latency engine configurations.",
            "link": "https://github.com/",
            "type": "ELITE EXPANSION",
            "color": "var(--accent-blue)"
        })

    # ── TAB LAYOUT PRESET PRESENTATIONS ──
    tab_courses, tab_projects = st.tabs(["📚 Dynamic Academic Integration", "💻 Automated Portfolio Targets"])

    with tab_courses:
        st.markdown("<h4 style='color: white; margin-bottom: 15px;'>Curated Educational Remediation Vectors</h4>", unsafe_allow_html=True)
        
        for gap in gap_recommendations:
            st.markdown(f"""
            <div class="card-glass" style="margin-bottom: 16px; border-left: 4px solid {gap['color']};">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <span style="background: rgba(255,255,255,0.05); color: {gap['color']}; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">{gap['type']}</span>
                        <h3 style="margin: 8px 0 4px 0; font-size: 18px;">{gap['title']}</h3>
                        <p style="color: var(--text-muted); font-size: 14px; margin: 0;">{gap['desc']}</p>
                    </div>
                    <a href="{gap['link']}" target="_blank" style="text-decoration: none;">
                        <button style="background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer;">
                            Launch External Hub →
                        </button>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_projects:
        st.markdown("<h4 style='color: white; margin-bottom: 15px;'>Dynamic Practical System Challenges</h4>", unsafe_allow_html=True)
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown(f"""
            <div class="card-glass" style="height: 100%;">
                <div style="font-size: 12px; color: var(--accent-blue); font-weight: 700; margin-bottom: 5px;">🔥 Recommended Integration Challenge</div>
                <h3 style="margin: 0 0 10px 0; font-size: 18px;">Automated Data-Inference Gateway</h3>
                <p style="color: var(--text-muted); font-size: 14px; line-height: 1.5; margin: 0 0 15px 0;">
                    Construct an asynchronous event ingestion broker tracking application states. Wire it using languages absent from your primary profile configuration.
                </p>
                <div style="font-size: 12px; color: var(--text-muted); border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
                    <strong>Target Objectives:</strong> Async Lifecycle • Schema Rigidity • Thread Locking
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_p2:
            st.markdown("""
            <div class="card-glass" style="height: 100%;">
                <div style="font-size: 12px; color: var(--accent-green); font-weight: 700; margin-bottom: 5px;">⚡ High-Density Impact Metric</div>
                <h3 style="margin: 0 0 10px 0; font-size: 18px;">Microservice Orchestration Sandbox</h3>
                <p style="color: var(--text-muted); font-size: 14px; line-height: 1.5; margin: 0 0 15px 0;">
                    Deploy an end-to-end container topology with health checks and metrics aggregations to explicitly demonstrate resource optimization on your CV.
                </p>
                <div style="font-size: 12px; color: var(--text-muted); border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
                    <strong>Target Objectives:</strong> Container Routing • Cluster Isolation • Instrumentation Logs
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
