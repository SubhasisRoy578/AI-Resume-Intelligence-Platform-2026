    # =====================================
    # SIDEBAR
    # =====================================

    with st.sidebar:
        st.markdown(
            f"""
            <div class='sidebar-welcome'>
                👋 Welcome back, <b>{st.session_state.username}</b>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")
        
        # Navigation Menu
        st.markdown("<p style='color:var(--gray-400);font-size:11px;text-transform:uppercase;letter-spacing:1px;font-weight:600;'>Navigation</p>", unsafe_allow_html=True)
        app_mode = st.radio(
            "",
            ["🔍 Single Resume Analyzer", "⚖️ Resume Comparator"],
            key="app_mode",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown(
            """
            <div style='padding:12px 16px;background:rgba(99,102,241,0.08);border-radius:12px;border:1px solid rgba(99,102,241,0.12);'>
                <p style='color:var(--gray-400);font-size:11px;margin:0;'>⚡ AI Resume Intelligence Platform</p>
                <p style='color:var(--gray-500);font-size:10px;margin:4px 0 0 0;'>v1.0 · Powered by Groq</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
