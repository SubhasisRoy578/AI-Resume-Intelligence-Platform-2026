<div align="center">

# 🚀 AI Resume Intelligence Platform

### An end-to-end AI + ML powered resume analysis platform

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.4-orange?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org)
[![Groq AI](https://img.shields.io/badge/Groq_AI-LLaMA_3.3_70B-purple?style=for-the-badge)](https://groq.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-green?style=for-the-badge&logo=sqlite)](https://sqlite.org)
[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Click_Here-brightgreen?style=for-the-badge)](https://ai-resume-intelligence-platform-wi3gfwjxxmpspjcc3onyac.streamlit.app/)

### 🔗 [LIVE DEMO →](https://ai-resume-intelligence-platform-wi3gfwjxxmpspjcc3onyac.streamlit.app/)

**Built by [Mommineedi Jahnavi Satya](https://github.com/M-jahnavi08)**

</div>

---

## 📸 Screenshots

### 🏠 Landing Page
![Landing Page](screenshots/landing.png)

### 🔐 Login & Signup
![Login](screenshots/login.png)

### 📊 Analytics Dashboard
![Dashboard](screenshots/dashboard.png)

### 🧠 ML Analysis — TF-IDF Job Match & Skill Gap
![ML Analysis](screenshots/ml_analysis.png)

### 🤖 AI Features — Powered by Groq LLaMA 3.3 70B
![AI Features](screenshots/ai_features.png)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 ATS Scoring | Rule-based ATS score using required skill matching |
| 🧠 ML Job Match | TF-IDF + Cosine Similarity for real ML-based job matching |
| 🔍 Skill Gap Analysis | Detects skills missing from JD using NLP |
| 📋 Section Detector | Checks resume structure (Education, Projects, etc.) |
| 🤖 AI Summary | Groq LLaMA 3.3 70B generated professional resume summary |
| 🔍 AI Feedback | Detailed recruiter-style resume feedback |
| ✉️ Cover Letter | AI-generated tailored cover letter |
| 🎯 Interview Prep | Personalized interview questions by difficulty level |
| 🚀 Recommendations | Career path, project, and skill recommendations |
| 🔐 Auth System | Secure login with PBKDF2-HMAC-SHA256 password hashing |
| 📂 History | Per-user resume analysis history with all scores |

---

## 🛠 Tech Stack

- **Frontend:** Streamlit, Custom CSS, Glassmorphism UI
- **AI:** Groq API — LLaMA 3.3 70B (ultra-fast inference)
- **ML:** scikit-learn (TF-IDF Vectorization, Cosine Similarity)
- **NLP:** Custom skill detection, keyword density, section parsing
- **Database:** SQLite (users + resume analytics)
- **PDF Parsing:** pdfplumber
- **Charts:** Plotly

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/M-jahnavi08/ai-resume-intelligence-platform.git
cd ai-resume-intelligence-platform

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Groq API key
# Edit .streamlit/secrets.toml:
# GROQ_API_KEY = "your_key_here"
# Get free key at: https://console.groq.com

# 4. Run
python -m streamlit run app.py
```

---

## 📁 Project Structure

```
resume-analyzer/
├── app.py                        # Main controller
├── components/
│   ├── dashboard.py              # ATS analytics dashboard
│   ├── ml_dashboard.py           # ML analysis dashboard
│   ├── ai_features.py            # Groq AI tools
│   ├── recommendations.py        # Career recommendations
│   ├── landing_page.py           # Landing page UI
│   └── auth_ui.py                # Login / Signup UI
├── utils/
│   ├── parser.py                 # PDF text extraction
│   ├── skill_engine.py           # Rule-based scoring
│   └── ml_engine.py              # TF-IDF ML engine
├── database/
│   ├── db.py                     # Resume database
│   └── auth_db.py                # User auth database
├── assets/
│   └── styles.css                # Full UI styling
├── screenshots/                  # Project screenshots
├── .streamlit/
│   └── secrets.toml              # API keys (not committed)
└── requirements.txt
```

---

## 🔒 Security

- Passwords hashed using **PBKDF2-HMAC-SHA256** with random salt
- 100,000 iterations — industry standard
- No plain-text passwords stored anywhere

---

## 🧠 ML Architecture

```
Resume PDF
    │
    ▼
Text Extraction (pdfplumber)
    │
    ├──► TF-IDF Vectorizer ──► Cosine Similarity ──► Job Match Score (40%)
    │
    ├──► Keyword Density Scoring ──► Skill Coverage %  (30%)
    │
    ├──► Section Detector (regex NLP) ──► Structure Score (30%)
    │
    └──► Weighted Combination ──► Final ML Resume Score
```

---

## 📊 Scoring System

| Score | Weight | Method |
|---|---|---|
| TF-IDF Job Match | 40% | scikit-learn cosine similarity |
| Keyword Density | 30% | Custom NLP frequency analysis |
| Section Quality | 30% | Regex-based section detection |

---

## 🌐 Deploy on Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Add `GROQ_API_KEY` in Secrets
5. Deploy — get a public URL instantly

---

## 👩‍💻 Developer

**Mommineedi Jahnavi Satya** — Built as a full-stack AI + ML portfolio project.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://linkedin.com/in/mommineedi-jahnavisatya-b8955a352)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/M-jahnavi08)
[![Live Demo](https://img.shields.io/badge/Live_Demo-🚀-brightgreen?style=flat)](https://ai-resume-intelligence-platform-wi3gfwjxxmpspjcc3onyac.streamlit.app/)
