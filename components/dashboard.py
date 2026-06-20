"""
Analytics Dashboard — ATS metrics, skill charts, and resume insights.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.skill_engine import score_label


def _metric_card(label: str, value: str, subtitle: str, color: str):
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);
                backdrop-filter:blur(14px);border-radius:20px;padding:28px 24px;
                text-align:center;border-top:3px solid {color}">
        <div style="font-size:12px;color:#94a3b8;text-transform:uppercase;
                    letter-spacing:1.5px;margin-bottom:10px">{label}</div>
        <div style="font-size:42px;font-weight:800;color:{color}">{value}</div>
        <div style="font-size:12px;color:#64748b;margin-top:6px">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def show_dashboard(text, detected_skills, ats_score, job_match_score,
                   strength_score, skill_bonus, resume_category, required_skills):

    st.markdown("<h2 style='color:white;margin-bottom:4px'>📊 Resume Analytics</h2>",
                unsafe_allow_html=True)
    st.markdown(f"<p style='color:#94a3b8;margin-bottom:24px'>"
                f"Detected category: <b style='color:#c084fc'>{resume_category}</b></p>",
                unsafe_allow_html=True)

    # ── Hero metrics ─────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        _metric_card("ATS Score", f"{ats_score:.1f}%",
                     score_label(ats_score), "#38bdf8")
    with c2:
        _metric_card("Job Match", f"{job_match_score:.1f}%",
                     score_label(job_match_score), "#818cf8")
    with c3:
        _metric_card("Strength", f"{strength_score}%",
                     score_label(strength_score), "#c084fc")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Skills ───────────────────────────────────────────────
    tab_skills, tab_charts, tab_text = st.tabs(
        ["🛠 Skills", "📈 Charts", "📄 Resume Text"]
    )

    with tab_skills:
        missing_skills = [s for s in required_skills if s not in detected_skills]

        col_det, col_mis = st.columns(2)
        with col_det:
            st.markdown("<h4 style='color:#22c55e'>✅ Detected Skills</h4>",
                        unsafe_allow_html=True)
            if detected_skills:
                # Render as pill badges
                pills = " ".join(
                    f"<span style='display:inline-block;background:rgba(34,197,94,0.12);"
                    f"border:1px solid rgba(34,197,94,0.3);border-radius:20px;"
                    f"padding:5px 14px;margin:4px;font-size:13px;color:#86efac'>{s}</span>"
                    for s in sorted(detected_skills)
                )
                st.markdown(f"<div style='line-height:2.2'>{pills}</div>",
                            unsafe_allow_html=True)
            else:
                st.caption("No skills detected.")

        with col_mis:
            st.markdown("<h4 style='color:#f87171'>❌ Missing Required Skills</h4>",
                        unsafe_allow_html=True)
            if missing_skills:
                pills = " ".join(
                    f"<span style='display:inline-block;background:rgba(239,68,68,0.10);"
                    f"border:1px solid rgba(239,68,68,0.3);border-radius:20px;"
                    f"padding:5px 14px;margin:4px;font-size:13px;color:#fca5a5'>{s}</span>"
                    for s in sorted(missing_skills)
                )
                st.markdown(f"<div style='line-height:2.2'>{pills}</div>",
                            unsafe_allow_html=True)
            else:
                st.success("All required skills found! 🎉")

    with tab_charts:
        # Radar / spider chart for score dimensions
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
            height=380,
            margin=dict(t=30, b=30),
            showlegend=False,
            title=dict(text="Resume Score Radar", font=dict(color='white', size=14))
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Bar — skills distribution
        if detected_skills:
            fig_pie = px.pie(
                names=detected_skills,
                values=[1] * len(detected_skills),
                title="Detected Skills Distribution",
                template="plotly_dark",
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                height=400,
                legend=dict(font=dict(size=11))
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab_text:
        st.markdown("<p style='color:#94a3b8;font-size:13px'>"
                    "Raw text extracted from your PDF.</p>",
                    unsafe_allow_html=True)
        st.text_area("Extracted Resume Text", value=text, height=400,
                     disabled=True, label_visibility="collapsed")
