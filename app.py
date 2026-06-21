# app.py
"""
ResumeIQ - Main Application Entry Point
Production-grade SaaS architecture.
"""
import streamlit as st
from components.auth_ui import show_auth_ui
from components.landing_page import show_landing_page
from components.dashboard import show_dashboard
from components.ai_features import show_ai_features
from components.recommendations import show_recommendations
from resume_compare import show_resume_compare

# 1. Page Configuration
st.set_page_config(
    page_title="ResumeIQ | AI Resume Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Inject Global CSS
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# 3. Session State Initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# 4. Routing Logic
def main():
    if not st.session_state.logged_in:
        # User not logged in: Show landing page or Auth UI
        show_landing_page()
        st.markdown("---")
        show_auth_ui()
    else:
        # User logged in: Show Dashboard Application
        st.sidebar.markdown(f"### 👤 {st.session_state.username}")
        page = st.sidebar.radio(
            "Navigation", 
            ["Dashboard", "AI Analysis", "Compare Resumes", "Recommendations"]
        )
        
        if page == "Dashboard":
            show_dashboard()
        elif page == "AI Analysis":
            show_ai_features()
        elif page == "Compare Resumes":
            show_resume_compare()
        elif page == "Recommendations":
            # Pass placeholder scores for demo logic
            show_recommendations(detected_skills=["Python", "AWS", "Docker"], ats_score=75, strength_score=80)
            
        if st.sidebar.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
