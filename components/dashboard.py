# components/dashboard.py
"""
Dashboard — High-level analytics with a focus on UX and clean visuals.
"""
import streamlit as st
import plotly.express as px
import pandas as pd

def show_dashboard():
    st.markdown("<h1 class='gradient-text'>⚡ Performance Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:var(--text-muted)'>Track your ATS optimization progress and skill development metrics.</p>", unsafe_allow_html=True)

    # ── Metric Cards (Grid Layout) ───────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="card-glass">
            <div style="font-size: 14px; color: var(--text-muted)">Overall Score</div>
            <div style="font-size: 32px; font-weight: 800; color: var(--accent-blue)">84%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card-glass">
            <div style="font-size: 14px; color: var(--text-muted)">ATS Match</div>
            <div style="font-size: 32px; font-weight: 800; color: var(--accent-purple)">78%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card-glass">
            <div style="font-size: 14px; color: var(--text-muted)">Skill Gap</div>
            <div style="font-size: 32px; font-weight: 800; color: var(--accent-green)">12%</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="card-glass">
            <div style="font-size: 14px; color: var(--text-muted)">Projects</div>
            <div style="font-size: 32px; font-weight: 800; color: white">05</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("##") # Spacing

    # ── Charts & Skills ──────────────────────────────────────
    c_left, c_right = st.columns([2, 1])

    with c_left:
        st.markdown("<div class='card-glass'>", unsafe_allow_html=True)
        st.subheader("ATS Score Trend")
        # Custom-themed Chart Logic
        df = pd.DataFrame({'Date': ['Jan', 'Feb', 'Mar', 'Apr'], 'Score': [60, 68, 75, 84]})
        fig = px.line(df, x='Date', y='Score', markers=True)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            yaxis=dict(showgrid=False),
            xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c_right:
        st.markdown("<div class='card-glass'>", unsafe_allow_html=True)
        st.subheader("Top Skills")
        skills = ["Python", "AWS", "Docker", "SQL", "Machine Learning"]
        for s in skills:
            st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03); padding:8px 12px; 
                border-radius:8px; margin-bottom:6px; border:1px solid rgba(255,255,255,0.05)">
                {s}
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Placeholder for future visual components
#
