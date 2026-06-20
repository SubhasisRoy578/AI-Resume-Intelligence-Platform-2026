import streamlit as st
import plotly.express as px

# =========================================
# SHOW DASHBOARD
# =========================================

def show_dashboard(

    text,

    detected_skills,

    ats_score,

    job_match_score,

    strength_score,

    skill_bonus,

    resume_category,

    required_skills
):

    # =====================================
    # TITLE
    # =====================================

    st.subheader(
        "📊 Resume Analytics Dashboard"
    )

    # =====================================
    # HERO METRICS
    # =====================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "ATS Score",

            f"{ats_score:.2f}%"
        )

    with col2:

        st.metric(

            "Job Match",

            f"{job_match_score:.2f}%"
        )

    with col3:

        st.metric(

            "Resume Strength",

            f"{strength_score}%"
        )

    # =====================================
    # CATEGORY
    # =====================================

    st.markdown("---")

    st.subheader(
        "🎯 Resume Category"
    )

    st.success(resume_category)

    # =====================================
    # DETECTED SKILLS
    # =====================================

    st.markdown("---")

    st.subheader(
        "🛠 Detected Skills"
    )

    for skill in detected_skills:

        st.success(skill)

    # =====================================
    # MISSING SKILLS
    # =====================================

    missing_skills = []

    for skill in required_skills:

        if skill not in detected_skills:

            missing_skills.append(skill)

    st.markdown("---")

    st.subheader(
        "❌ Missing Skills"
    )

    if len(missing_skills) > 0:

        for skill in missing_skills:

            st.warning(skill)

    else:

        st.success(
            "No important skills missing."
        )

    # =====================================
    # EXTRACTED TEXT
    # =====================================

    st.markdown("---")

    with st.expander(
        "View Extracted Resume Text"
    ):

        st.write(text)

    # =====================================
    # ANALYTICS DASHBOARD
    # =====================================

    st.markdown("---")

    st.subheader(
        "📈 Analytics Dashboard"
    )

    # =====================================
    # PIE CHART
    # =====================================

    skill_data = {

        "Skill": detected_skills,

        "Count": [1] * len(detected_skills)
    }

    fig1 = px.pie(

        skill_data,

        names="Skill",

        values="Count",

        title="Detected Skills Distribution",

        template="plotly_dark"
    )

    fig1.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font_color="white",

        height=450
    )

    # =====================================
    # ATS CHART
    # =====================================

    ats_data = {

        "Category": ["ATS Score"],

        "Score": [ats_score]
    }

    fig2 = px.bar(

        ats_data,

        x="Category",

        y="Score",

        text="Score",

        title="ATS Score Analysis",

        template="plotly_dark"
    )

    fig2.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font_color="white",

        height=450
    )

    # =====================================
    # CHART COLUMNS
    # =====================================

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:

        st.plotly_chart(

            fig1,

            use_container_width=True
        )

    with col_chart2:

        st.plotly_chart(

            fig2,

            use_container_width=True
        )

    # =====================================
    # JOB MATCH CHART
    # =====================================

    job_data = {

        "Category": ["Job Match"],

        "Score": [job_match_score]
    }

    fig3 = px.bar(

        job_data,

        x="Category",

        y="Score",

        text="Score",

        title="Resume vs Job Match",

        template="plotly_dark"
    )

    fig3.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font_color="white",

        height=450
    )

    st.plotly_chart(

        fig3,

        use_container_width=True
    )

    # =====================================
    # RESUME STRENGTH CHART
    # =====================================

    strength_data = {

        "Metric": [

            "ATS Score",

            "Job Match",

            "Skill Bonus"
        ],

        "Value": [

            ats_score,

            job_match_score,

            skill_bonus
        ]
    }

    fig4 = px.bar(

        strength_data,

        x="Metric",

        y="Value",

        text="Value",

        title="Resume Strength Analysis",

        template="plotly_dark"
    )

    fig4.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font_color="white",

        height=450
    )

    st.plotly_chart(

        fig4,

        use_container_width=True
    )
