"""
Recommendations — project ideas, resume tips, and career roadmap
based on detected skills and scores.
"""

import streamlit as st

# =========================================
# PROJECT DATABASE
# =========================================

PROJECT_DB = {
    # AI / ML
    ("Python", "Machine Learning"): [
        "AI Resume Analyzer (like this one!)",
        "Fake News Detection System",
        "Movie Recommendation Engine",
        "Student Performance Predictor",
        "Sentiment Analysis Dashboard",
    ],
    ("TensorFlow",): [
        "Image Classification App",
        "Transfer Learning Image Classifier",
        "Neural Style Transfer Web App",
    ],
    ("NLP",): [
        "AI Chatbot with Memory",
        "Text Summarizer API",
        "Multilingual Sentiment Analyzer",
    ],
    # Web
    ("React",): [
        "Personal Portfolio with Blog",
        "Real-Time Chat Application",
        "Task Management Dashboard",
        "E-Commerce Storefront",
    ],
    ("Node.js",): [
        "REST API with JWT Auth",
        "WebSocket Notification System",
        "GraphQL Server + Client",
    ],
    # Cloud / DevOps
    ("Docker",): [
        "Dockerized Flask Microservices",
        "CI/CD Pipeline with GitHub Actions",
        "Container Monitoring Dashboard",
    ],
    ("AWS",): [
        "Serverless Resume API (Lambda)",
        "S3 Media Manager Web App",
        "Cloud Cost Optimiser Dashboard",
    ],
    # Data
    ("Pandas", "NumPy"): [
        "COVID-19 Data Visualiser",
        "Stock Price Trend Analyser",
        "Sales Forecasting Dashboard",
    ],
}

CAREER_PATHS = {
    "Machine Learning":    ("AI / ML Engineer",    "#c084fc",
        ["Complete a Kaggle competition", "Get AWS ML Specialty cert",
         "Contribute to a Hugging Face model", "Build an end-to-end ML pipeline"]),
    "React":               ("Full Stack Developer", "#38bdf8",
        ["Build a SaaS side-project", "Learn Next.js + TypeScript",
         "Get a cloud deployment live", "Contribute to an open-source UI library"]),
    "AWS":                 ("Cloud Engineer",       "#34d399",
        ["Get AWS Solutions Architect cert", "Set up a multi-region deployment",
         "Build an IaC stack with Terraform", "Implement a zero-downtime deploy"]),
    "Data Science":        ("Data Scientist",       "#fb923c",
        ["Publish a Kaggle notebook", "Learn Spark for big data",
         "Complete a BI certification", "Build a predictive analytics API"]),
    "Docker":              ("DevOps Engineer",      "#818cf8",
        ["Set up a K8s cluster", "Implement GitOps with ArgoCD",
         "Build a monitoring stack", "Automate infra with Ansible"]),
}


def _project_pill(text: str):
    st.markdown(
        f"<div style='background:rgba(129,140,248,0.10);border:1px solid rgba(129,140,248,0.25);"
        f"border-radius:12px;padding:10px 16px;margin-bottom:8px;color:#c7d2fe;"
        f"font-size:14px'>🔨 {text}</div>",
        unsafe_allow_html=True
    )


def _tip_pill(text: str, color="#34d399"):
    st.markdown(
        f"<div style='background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.2);"
        f"border-left:3px solid {color};border-radius:10px;padding:10px 16px;"
        f"margin-bottom:8px;color:#a7f3d0;font-size:13px'>→ {text}</div>",
        unsafe_allow_html=True
    )


def show_recommendations(detected_skills: list, ats_score: float,
                          strength_score: float):

    st.markdown("<h2 style='color:white'>🚀 Personalised Recommendations</h2>",
                unsafe_allow_html=True)

    tab_proj, tab_improve, tab_career = st.tabs(
        ["💡 Projects", "📈 Resume Tips", "🛣 Career Path"]
    )

    # ── Projects ─────────────────────────────────────────────
    with tab_proj:
        recommended = []
        for key_skills, projects in PROJECT_DB.items():
            if all(s in detected_skills for s in key_skills):
                recommended.extend(projects)
        recommended = list(dict.fromkeys(recommended))  # dedupe, preserve order

        if recommended:
            st.markdown("<p style='color:#94a3b8'>Projects matched to your skill set:</p>",
                        unsafe_allow_html=True)
            for p in recommended[:10]:
                _project_pill(p)
        else:
            st.info("Add more technical skills to unlock project recommendations.")

    # ── Resume improvement ───────────────────────────────────
    with tab_improve:
        tips = []
        if ats_score < 70:
            tips.append("Add more required keywords explicitly — ATS systems need exact matches.")
        if strength_score < 70:
            tips.append("Add 2–3 real-world projects with quantified outcomes (e.g. '20% accuracy improvement').")
        if "Git" not in detected_skills:
            tips.append("Add Git/GitHub to your skills — it's required for nearly every tech role.")
        if "SQL" not in detected_skills:
            tips.append("SQL is a fundamental skill. Even a brief mention or project improves hirability.")
        if "Docker" not in detected_skills:
            tips.append("Docker knowledge differentiates you for backend and DevOps roles.")
        if len(detected_skills) < 8:
            tips.append("Your resume lists few skills. Expand your Skills section with relevant technologies.")

        # General tips always shown
        tips += [
            "Quantify achievements: use numbers, percentages, and impact metrics.",
            "Keep resume to 1 page for under 3 years experience; 2 pages max otherwise.",
            "Use action verbs: Built, Designed, Led, Reduced, Improved, Deployed.",
            "Tailor your summary paragraph for each job application.",
        ]

        for tip in tips:
            _tip_pill(tip)

    # ── Career path ──────────────────────────────────────────
    with tab_career:
        matched_path = None
        for skill, (title, color, milestones) in CAREER_PATHS.items():
            if skill in detected_skills:
                matched_path = (title, color, milestones)
                break

        if matched_path:
            title, color, milestones = matched_path
            st.markdown(
                f"<div style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);"
                f"border-left:4px solid {color};border-radius:16px;padding:20px 24px;margin-bottom:24px'>"
                f"<div style='font-size:13px;color:#94a3b8;text-transform:uppercase;letter-spacing:1px'>"
                f"Recommended Career</div>"
                f"<div style='font-size:28px;font-weight:800;color:{color};margin:8px 0'>{title}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
            st.markdown("<h4 style='color:white'>Next Steps to Land the Role</h4>",
                        unsafe_allow_html=True)
            for i, step in enumerate(milestones, 1):
                st.markdown(
                    f"<div style='background:rgba(255,255,255,0.04);border-radius:12px;"
                    f"padding:12px 18px;margin-bottom:8px;color:#e2e8f0'>"
                    f"<b style='color:{color}'>{i}.</b> {step}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.info("Add specialised skills (ML, React, AWS, Docker, Data Science) "
                    "to get a tailored career roadmap.")
