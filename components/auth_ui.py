# components/auth_ui.py
"""
Authentication UI — Modern login/signup modal with focus states and clean layout.
"""
import streamlit as st

def show_auth_ui():
    st.markdown("""
    <style>
        .auth-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 40px;
            background: var(--card-bg);
            border: var(--card-border);
            backdrop-filter: var(--glass-blur);
            border-radius: var(--radius-lg);
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    st.subheader("Welcome Back")
    st.markdown("<p style='color:var(--text-muted); margin-bottom: 24px;'>Sign in to access your ResumeIQ dashboard.</p>", unsafe_allow_html=True)

    with st.form("auth_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        submitted = st.form_submit_button("Sign In")
        
        if submitted:
            if username and password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Please provide both fields.")
    
    st.markdown("</div>", unsafe_allow_html=True)
