# components/landing_page.py
"""
Landing Page — High-conversion UI with clean typography and modern call-to-actions.
"""
import streamlit as st

def show_landing_page():
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <h1 style="font-size: 56px; margin-bottom: 20px;">
            Land Your Dream Job with <span class="gradient-text">AI Intelligence</span>
        </h1>
        <p style="font-size: 20px; color: var(--text-muted); max-width: 700px; margin: 0 auto 40px;">
            Stop guessing why your resume isn't getting attention. 
            Get real-time feedback, skill gap analysis, and personalized career roadmaps.
        </p>
        <div style="display: flex; gap: 16px; justify-content: center;">
            <button style="background: var(--accent-blue); border: none; padding: 12px 32px; 
            border-radius: 8px; color: white; font-weight: 600; cursor: pointer;">
                Get Started Free →
            </button>
            <button style="background: transparent; border: 1px solid var(--text-muted); padding: 12px 32px; 
            border-radius: 8px; color: white; cursor: pointer;">
                View Demo
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature Grid
    st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>Everything You Need</h2>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    features = [
        ("⚡ Real-time ATS Analysis", "Get instant feedback on your resume keywords and formatting."),
        ("🎯 Skill Gap Detection", "Identify exactly what skills you're missing for specific roles."),
        ("🛣 Career Roadmaps", "Follow curated paths to upskill and land your next role faster.")
    ]

    for i, (title, desc) in enumerate(features):
        with cols[i]:
            st.markdown(f"""
            <div class="card-glass" style="height: 200px;">
                <h3 style="margin-top: 0;">{title}</h3>
                <p style="color: var(--text-muted);">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
