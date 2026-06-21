"""
Analytics Dashboard — ATS metrics, skill charts, and resume insights.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.skill_engine import score_label


def _metric_card(label: str, value: str, subtitle: str, color: str, icon: str = ""):
    """Professional metric card with icon and gradient border"""
    st.markdown(f"""
    <div class="metric-card animate-fade-up">
        <div style="font-size:24px;margin-bottom:8px;">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{color}">{value}</div>
        <div class="metric-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def show_dashboard(text, detected_skills, ats_score, job_match_score,
                   strength_score, skill_bonus, resume_category, required_skills):

    st.markdown("<h2 style='color:white;margin-bottom:4px;font-weight:800;'>📊 Resume Analytics</h2>",
                unsafe_allow_html=True)
    st.markdown(f"""
        <p style='color:var(--gray-400);margin-bottom:24px;font-size:16px;'>
            Detected category: <span style='color:var(--purple-400);font-weight:600;'>{resume_category}</span>
            · {len(detected_skills)} skills found
        </p>
    """, unsafe_allow_html=True)

    # ── Hero metrics ─────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        _metric_card("ATS Score", f"{ats_score:.1f}%",
                     score_label(ats_score), "#38bdf8", "🎯")
    with c2:
        _metric_card("Job Match", f"{job_match_score:.1f}%",
                     score_label(job_match_score), "#818cf8", "📊")
    with c3:
        _metric_card("Strength", f"{strength_score:.1f}%",
                     score_label(strength_score), "#c084fc", "💪")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Skills ───────────────────────────────────────────────
    tab_skills, tab_charts, tab_text = st.tabs(
        ["🛠 Skills", "📈 Charts", "📄 Resume Text"]
    )

    with tab_skills:
        missing_skills = [s for s in required_skills if s not in detected_skills]

        col_det, col_mis = st.columns(2)
        with col_det:
            st.markdown("<h4 style='color:#22c55e;font-weight:700;'>✅ Detected Skills</h4>",
                        unsafe_allow_html=True)
            if detected_skills:
                pills = " ".join(
                    f"<span class='skill-pill'>{s}</span>"
                    for s in sorted(detected_skills)
                )
                st.markdown(f"<div style='line-height:2.4'>{pills}</div>",
                            unsafe_allow_html=True)
            else:
                st.caption("No skills detected.")

        with col_mis:
            st.markdown("<h4 style='color:#f87171;font-weight:700;'>❌ Missing Required Skills</h4>",
                        unsafe_allow_html=True)
            if missing_skills:
                pills = " ".join(
                    f"<span class='skill-pill-missing'>{s}</span>"
                    for s in sorted(missing_skills)
                )
                st.markdown(f"<div style='line-height:2.4'>{pills}</div>",
                            unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.2);
                                border-radius:12px;padding:16px;text-align:center;'>
                        <span style='color:#22c55e;font-size:18px;'>🎉 All required skills found!</span>
                    </div>
                """, unsafe_allow_html=True)

    with tab_charts:
        # Radar chart
        categories = ["ATS Score", "Job Match", "Strength",
                       "Skill Count (×5)", "Section Bonus"]
        values = [
            ats_score,
            job_match_score,
            strength_score,
            min(len(detected_skills) * 5, 100),
            skill_bonus * 5,
        ]
        
        fig_radar = go.Figure(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line=dict(color='#818cf8', width=2),
            fillcolor='rgba(129,140,248,0.15)'
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, range=[0, 100],
                                gridcolor='rgba(255,255,255,0.08)',
                                color='#64748b'),
                angularaxis=dict(gridcolor='rgba(255,255,255,0.08)',
                                  color='#94a3b8')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400,
            margin=dict(t=30, b=30),
            showlegend=False,
            title=dict(text="Resume Score Radar", font=dict(color='white', size=16, weight=700))
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Bar chart - skills distribution
        if detected_skills:
            # Show top skills with values
            skill_counts = {s: 1 for s in detected_skills[:12]}
            fig_bar = px.bar(
                x=list(skill_counts.keys()),
                y=list(skill_counts.values()),
                title="Skills Distribution",
                template="plotly_dark",
                color_discrete_sequence=["#818cf8"],
                labels={'x': 'Skills', 'y': 'Presence'}
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                height=350,
                showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)",
                title_font=dict(size=16, weight=700)
            )
            fig_bar.update_xaxis(gridcolor='rgba(255,255,255,0.05)')
            fig_bar.update_yaxis(gridcolor='rgba(255,255,255,0.05)')
            st.plotly_chart(fig_bar, use_container_width=True)

    with tab_text:
        st.markdown("""
            <p style='color:var(--gray-400);font-size:13px;margin-bottom:12px;'>
                📄 Raw text extracted from your PDF.
            </p>
        """, unsafe_allow_html=True)
        st.text_area("Extracted Resume Text", value=text, height=400,
                     disabled=True, label_visibility="collapsed")
