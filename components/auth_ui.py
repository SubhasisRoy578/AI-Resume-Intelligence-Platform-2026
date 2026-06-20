import streamlit as st
from database.auth_db import register_user, login_user

# =========================================
# AUTH UI
# =========================================

def show_auth_ui():

    st.markdown(
        """
        <div class="auth-wrapper">
            <div class="auth-main-title">Access Your AI Dashboard</div>
            <div class="auth-subtitle">
                Login or create an account to unlock AI-powered resume intelligence.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    left_col, center_col, right_col = st.columns([1, 2, 1])

    with center_col:

        auth_tab1, auth_tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

        # =================================
        # LOGIN
        # =================================
        with auth_tab1:
            st.markdown("<h2 class='auth-title'>Welcome Back</h2>", unsafe_allow_html=True)

            username = st.text_input("Username", key="login_username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")

            if st.button("🔐 Login", use_container_width=True, key="btn_login"):
                if not username.strip() or not password.strip():
                    st.error("Please fill in both fields.")
                else:
                    success, msg = login_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = username.strip()
                        st.rerun()
                    else:
                        st.error(msg)

        # =================================
        # SIGNUP
        # =================================
        with auth_tab2:
            st.markdown("<h2 class='auth-title'>Create Account</h2>", unsafe_allow_html=True)

            new_username = st.text_input("Username", key="signup_username", placeholder="Min 3 characters")
            new_password = st.text_input("Password", type="password", key="signup_password", placeholder="Min 6 characters")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm", placeholder="Repeat password")

            if st.button("🚀 Create Account", use_container_width=True, key="btn_signup"):
                if not new_username.strip() or not new_password.strip():
                    st.error("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, msg = register_user(new_username, new_password)
                    if success:
                        st.success(msg + " Please login.")
                    else:
                        st.error(msg)
