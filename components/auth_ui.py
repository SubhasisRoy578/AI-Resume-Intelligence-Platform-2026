"""
Auth UI — Login and Sign Up with clean error states.
"""

import streamlit as st
from database.auth_db import register_user, login_user


def show_auth_ui():

    st.markdown("""
    <div class="auth-wrapper">
        <div class="auth-main-title">Access Your Dashboard</div>
        <div class="auth-subtitle">
            Log in or create a free account to unlock AI-powered resume analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 2, 1])

    with center:
        login_tab, signup_tab = st.tabs(["🔐 Log In", "📝 Sign Up"])

        # ── Login ─────────────────────────────────────────────
        with login_tab:
            st.markdown("<h3 class='auth-title'>Welcome back</h3>",
                        unsafe_allow_html=True)
            username = st.text_input("Username", key="li_user",
                                      placeholder="Your username")
            password = st.text_input("Password", type="password",
                                      key="li_pass", placeholder="Your password")
            if st.button("Log In →", use_container_width=True, key="btn_login"):
                if not username.strip() or not password.strip():
                    st.error("Please fill in both fields.")
                else:
                    ok, msg = login_user(username, password)
                    if ok:
                        st.session_state.logged_in = True
                        st.session_state.username = username.strip()
                        st.rerun()
                    else:
                        st.error(msg)

        # ── Sign up ───────────────────────────────────────────
        with signup_tab:
            st.markdown("<h3 class='auth-title'>Create account</h3>",
                        unsafe_allow_html=True)
            new_user = st.text_input("Username", key="su_user",
                                      placeholder="Min 3 characters, letters/numbers/-/_")
            new_pass = st.text_input("Password", type="password",
                                      key="su_pass", placeholder="Min 6 characters")
            confirm  = st.text_input("Confirm Password", type="password",
                                      key="su_conf", placeholder="Repeat password")
            if st.button("Create Account →", use_container_width=True, key="btn_signup"):
                if not new_user.strip() or not new_pass.strip():
                    st.error("Please fill in all fields.")
                elif new_pass != confirm:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = register_user(new_user, new_pass)
                    if ok:
                        st.success(msg + " You can now log in.")
                    else:
                        st.error(msg)
