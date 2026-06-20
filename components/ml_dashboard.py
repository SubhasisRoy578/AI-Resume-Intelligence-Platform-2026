import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# =========================================
# ML DASHBOARD
# =========================================

def show_ml_dashboard(ml_results: dict, detected_skills: list, job_description: str):

    st.markdown("<h2 class='section-title' style='font-size:32px;margin-top:10px'>🧠 ML Analysis Results</h2>", unsafe_allow_html=True)

    # =====================================
    # TOP ML SCORE CARDS
    # =====================================

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class='ml-score-card'>
                <div class='ml-score-label'>ML Resume Score</div>
                <div class='ml-score-value'>{ml_results['ml_score']}%</div>
                <div class='ml-score-sub'>Combined AI + ML signal</div>
            </div>
            """, unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class='ml-score-card'>
                <div class='ml-score-label'>TF-IDF Job Match</div>
                <div class='ml-score-value'>{ml_results['tfidf_score']}%</div>
                <div class='ml-score-sub'>Cosine similarity score</div>
            </div>
            """, unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class='ml-score-card'>
                <div class='ml-score-label'>Section Quality</div>
                <div class='ml-score-value'>{ml_results['section_score']}%</div>
                <div class='ml-score-sub'>Resume structure score</div>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # RESUME SECTIONS DETECTED
    # =====================================

    st.markdown("<h3 style='color:white'>📋 Resume Sections Detected</h3>", unsafe_allow_html=True)

    sections = ml_results.get("sections", {})
    sec_cols = st.columns(len(sections))

    for col, (section, present) in zip(sec_cols, sections.items()):
        icon = "✅" if present else "❌"
        color = "#22c55e" if present else "#ef4444"
        with col:
            st.markdown(
                f"""
                <div class='section-pill' style='border-color:{color}'>
                    {icon} {section.capitalize()}
                </div>
                """, unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # SKILL GAP ANALYSIS
    # =====================================

    gap = ml_results.get("gap_result", {})
    missing = gap.get("missing_skills", [])

    st.markdown("<h3 style='color:white'>🔍 Skill Gap Analysis</h3>", unsafe_allow_html=True)

    if missing:
        st.markdown(
            f"<p style='color:#94a3b8'>Your resume is missing <b style='color:#f87171'>{len(missing)}</b> skills from the job description. Add these to improve your match:</p>",
            unsafe_allow_html=True
        )
        gap_cols = st.columns(min(len(missing), 4))
        for i, skill in enumerate(missing[:8]):
            with gap_cols[i % 4]:
                st.markdown(
                    f"<div class='gap-pill'>⚡ {skill}</div>",
                    unsafe_allow_html=True
                )
    elif job_description.strip():
        st.success("✅ No skill gaps detected — your resume covers the job description well!")
    else:
        st.info("Paste a job description above to see skill gap analysis.")

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # ML SCORE BREAKDOWN CHART
    # =====================================

    st.markdown("<h3 style='color:white'>📊 ML Score Breakdown</h3>", unsafe_allow_html=True)

    fig = go.Figure(go.Bar(
        x=["TF-IDF Match", "Keyword Density", "Section Quality"],
        y=[ml_results["tfidf_score"], ml_results["density_score"], ml_results["section_score"]],
        marker=dict(
            color=["#38bdf8", "#818cf8", "#c084fc"],
            line=dict(width=0)
        ),
        text=[f"{v}%" for v in [ml_results["tfidf_score"], ml_results["density_score"], ml_results["section_score"]]],
        textposition="outside",
        textfont=dict(color="white", size=14)
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=350,
        margin=dict(t=20, b=20),
        yaxis=dict(range=[0, 110], gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(gridcolor="rgba(0,0,0,0)")
    )

    st.plotly_chart(fig, use_container_width=True)

    # =====================================
    # KEYWORD FREQUENCY
    # =====================================

    keyword_freq = ml_results.get("keyword_freq", {})
    if keyword_freq:
        st.markdown("<h3 style='color:white'>🔑 Keyword Frequency in Resume</h3>", unsafe_allow_html=True)

        freq_fig = px.bar(
            x=list(keyword_freq.keys()),
            y=list(keyword_freq.values()),
            labels={"x": "Skill", "y": "Mentions"},
            template="plotly_dark",
            color=list(keyword_freq.values()),
            color_continuous_scale="Viridis"
        )
        freq_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            height=300,
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(t=10, b=10)
        )
        st.plotly_chart(freq_fig, use_container_width=True)
