import streamlit as st

# =========================================
# SHOW RECOMMENDATIONS
# =========================================

def show_recommendations(

    detected_skills,

    ats_score,

    strength_score
):

    st.subheader(
        "🚀 Recommendations"
    )

    st.markdown("---")

    # =====================================
    # PROJECT RECOMMENDATIONS
    # =====================================

    recommended_projects = []

    # AI / ML PROJECTS

    if (

        "Python" in detected_skills
        and
        "Machine Learning" in detected_skills

    ):

        recommended_projects.extend([

            "AI Resume Analyzer",

            "Fake News Detection System",

            "Movie Recommendation System",

            "AI Chatbot using NLP",

            "Student Performance Predictor"
        ])

    # WEB DEVELOPMENT PROJECTS

    if (

        "React" in detected_skills
        or
        "JavaScript" in detected_skills

    ):

        recommended_projects.extend([

            "Portfolio Website",

            "Task Management App",

            "E-Commerce Website",

            "Real-Time Chat Application"
        ])

    # CLOUD PROJECTS

    if (

        "AWS" in detected_skills
        or
        "Docker" in detected_skills

    ):

        recommended_projects.extend([

            "Dockerized Flask App",

            "CI/CD Deployment Pipeline",

            "Cloud Monitoring Dashboard"
        ])

    # REMOVE DUPLICATES

    recommended_projects = list(
        set(recommended_projects)
    )

    # =====================================
    # DISPLAY PROJECTS
    # =====================================

    st.subheader(
        "💡 Recommended Projects"
    )

    if len(recommended_projects) > 0:

        for project in recommended_projects:

            st.success(project)

    else:

        st.info(
            "Add more technical skills for better project recommendations."
        )

    st.markdown("---")

    # =====================================
    # RESUME IMPROVEMENT SUGGESTIONS
    # =====================================

    st.subheader(
        "📈 Resume Improvement Suggestions"
    )

    suggestions = []

    if ats_score < 70:

        suggestions.append(
            "Improve ATS score by adding more technical keywords."
        )

    if strength_score < 70:

        suggestions.append(
            "Build stronger real-world projects."
        )

    if "Git" not in detected_skills:

        suggestions.append(
            "Add GitHub projects to strengthen your profile."
        )

    if "SQL" not in detected_skills:

        suggestions.append(
            "Learn SQL for better placement opportunities."
        )

    if "Docker" not in detected_skills:

        suggestions.append(
            "Learning Docker can improve DevOps opportunities."
        )

    if len(suggestions) > 0:

        for suggestion in suggestions:

            st.info(suggestion)

    else:

        st.success(
            "Your resume looks strong overall."
        )

    st.markdown("---")

    # =====================================
    # CAREER ROADMAP
    # =====================================

    st.subheader(
        "🛣 Suggested Career Path"
    )

    if (

        "Machine Learning" in detected_skills

    ):

        st.success(
            "Recommended Career: AI / ML Engineer"
        )

    elif (

        "React" in detected_skills

    ):

        st.success(
            "Recommended Career: Full Stack Developer"
        )

    elif (

        "AWS" in detected_skills

    ):

        st.success(
            "Recommended Career: Cloud Engineer"
        )

    else:

        st.info(
            "Explore multiple technology domains to identify your best career path."
        )
