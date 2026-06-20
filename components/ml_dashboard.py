"""
ML Dashboard — TF-IDF scores, skill gap analysis, section detection.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def show_ml_dashboard(ml_results: dict, detected_skills: list,
                       job_description: str):

    st.markdown(
        "<h2 style='color:white;margin-bottom:4px'>🧠 ML Analysis Results</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<p style='color:#94a3b8;margin-bottom:24px'>"
        f"{ml_results.get('explanation', 'Machine learning resume analysis.')}</p>",
        unsafe_allow_html=True
    )

    # ── Top score cards ───────────────────────────────────────
    c1, c2, c3 = st.columns(3)

    def _card(col, label, val, sub, color):
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);
                        backdrop-filter:blur(14px);border-radius:20px;padding:28px 24px;
                        text-align:center;border-top:3px solid {color};margin-bottom:10px">
                <div style="font-size:11px;color:#94a3b8;text-transform:uppercase;
                            letter-spacing:1.5px;margin-bottom:8px">{label}</div>
                <div style="font-size:40px;font-weight:800;color:{color}">{val}%</div>
                <div style="font-size:11px;color:#64748b;margin-top:6px">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    _card(c1, "ML Resume Score",  ml_results["ml_score"],
          "Combined ML signal", "#c084fc")
    _card(c2, "TF-IDF Job Match", ml_results["tfidf_score"],
          "Cosine similarity",  "#818cf8")
    _card(c3, "Section Quality",  ml_results["section_score"],
          "Structure score",    "#38bdf8")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Section detector ──────────────────────────────────────
    st.markdown("<h3 style='color:white'>📋 Resume Sections</h3>",
                unsafe_allow_html=True)
    sections = ml_results.get("sections", {})
    cols = st.columns(len(sections))
    for col, (sec, present) in zip(cols, sections.items()):
        icon, color = ("✅", "#22c55e") if present else ("❌", "#ef4444")
        with col:
            st.markdown(
                f"<div style='border:1.5px solid {color};border-radius:12px;"
                f"padding:10px 14px;text-align:center;font-size:13px;color:white;"
                f"background:rgba(255,255,255,0.04)'>{icon} {sec.capitalize()}</div>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Skill gap ─────────────────────────────────────────────
    gap = ml_results.get("gap_result", {})
    missing = gap.get("missing_skills", [])
    st.markdown("<h3 style='color:white'>🔍 Skill Gap Analysis</h3>",
                unsafe_allow_html=True)

    if missing:
        total_jd = gap.get("jd_skills_total", len(missing))
        coverage = round((1 - len(missing) / total_jd) * 100) if total_jd else 0
        st.markdown(
            f"<p style='color:#94a3b8'>Covering "
            f"<b style='color:#34d399'>{coverage}%</b> of JD skills. "
            f"Missing <b style='color:#f87171'>{len(missing)}</b> skill(s):</p>",
            unsafe_allow_html=True
        )
        chunk_size = 4
        for i in range(0, min(len(missing), 8), chunk_size):
            chunk = missing[i:i + chunk_size]
            gcols = st.columns(chunk_size)
            for j, skill in enumerate(chunk):
                with gcols[j]:
                    st.markdown(
                        f"<div style='background:rgba(239,68,68,0.10);"
                        f"border:1px solid rgba(239,68,68,0.3);border-radius:12px;"
                        f"padding:10px 14px;text-align:center;font-size:13px;"
                        f"color:#fca5a5'>⚡ {skill}</div>",
                        unsafe_allow_html=True
                    )
    elif job_description.strip():
        st.success("✅ No skill gaps — your resume covers the JD well!")
    else:
        st.info("Paste a job description to see skill gap analysis.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Score breakdown chart ─────────────────────────────────
    st.markdown("<h3 style='color:white'>📊 ML Score Breakdown</h3>",
                unsafe_allow_html=True)

    fig = go.Figure(go.Bar(
        x=["TF-IDF Match", "Keyword Density", "Section Quality"],
        y=[ml_results["tfidf_score"],
           ml_results["density_score"],
           ml_results["section_score"]],
        marker=dict(
            color=["#38bdf8", "#818cf8", "#c084fc"],
            line=dict(width=0)
        ),
        text=[f"{v:.1f}%" for v in [ml_results["tfidf_score"],
                                      ml_results["density_score"],
                                      ml_results["section_score"]]],
        textposition="outside",
        textfont=dict(color="white", size=14)
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=340,
        margin=dict(t=20, b=10),
        yaxis=dict(range=[0, 115], gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(gridcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Keyword frequency ─────────────────────────────────────
    keyword_freq = ml_results.get("keyword_freq", {})
    if keyword_freq:
        st.markdown("<h3 style='color:white'>🔑 Keyword Frequency</h3>",
                    unsafe_allow_html=True)
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
            height=290,
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(t=10, b=10)
        )
        st.plotly_chart(freq_fig, use_container_width=True)
