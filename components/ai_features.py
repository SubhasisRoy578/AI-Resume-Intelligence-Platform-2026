import streamlit as st
from groq import Groq

# =========================================
# AI FEATURES — Powered by Groq
# =========================================

def show_ai_features(api_key: str, text: str):

    st.markdown("<h2 style='color:white'>🤖 AI Resume Features</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8'>Powered by Groq AI — Ultra fast inference</p>", unsafe_allow_html=True)

    if not text.strip():
        st.warning("No resume text detected. Please upload a valid PDF.")
        return

    def call_groq(prompt: str, spinner_msg: str):
        try:
            with st.spinner(spinner_msg):
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert resume analyst, career coach, and professional writer."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=1024,
                    temperature=0.7
                )
                return response.choices[0].message.content
        except Exception as e:
            st.error(f"Groq API error: {str(e)}")
            return None

    st.markdown("---")

    # =====================================
    # AI RESUME SUMMARY
    # =====================================

    st.markdown("<h3 style='color:white'>📝 AI Resume Summary</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8'>Generates a professional ATS-optimized summary from your resume.</p>", unsafe_allow_html=True)

    if st.button("✨ Generate Resume Summary", use_container_width=True, key="btn_summary"):
        result = call_groq(
            f"""Generate a concise, professional, ATS-friendly resume summary (3-5 sentences) for this candidate.
Focus on their strongest skills, experience, and value proposition.

Resume:
{text}""",
            "Generating AI summary..."
        )
        if result:
            st.success("Summary Generated!")
            st.markdown(f"<div class='ai-output-card'>{result}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # =====================================
    # AI RESUME FEEDBACK
    # =====================================

    st.markdown("<h3 style='color:white'>🔍 AI Resume Feedback</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8'>Get detailed, actionable feedback to improve your resume.</p>", unsafe_allow_html=True)

    if st.button("🔍 Analyze & Get Feedback", use_container_width=True, key="btn_feedback"):
        result = call_groq(
            f"""Analyze this resume and provide structured feedback with:
1. Overall Strengths (2-3 points)
2. Key Weaknesses (2-3 points)
3. Specific Improvements (bullet points)
4. ATS Optimization Tips
5. Overall Rating out of 10

Be direct, specific, and actionable.

Resume:
{text}""",
            "Analyzing your resume..."
        )
        if result:
            st.success("Feedback Ready!")
            st.markdown(f"<div class='ai-output-card'>{result}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # =====================================
    # AI COVER LETTER
    # =====================================

    st.markdown("<h3 style='color:white'>✉️ AI Cover Letter Generator</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8'>Generate a tailored cover letter for any job.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        job_role = st.text_input("Job Role", placeholder="e.g. Machine Learning Engineer", key="cover_role")
    with col2:
        company_name = st.text_input("Company Name", placeholder="e.g. Google", key="cover_company")

    if st.button("✉️ Generate Cover Letter", use_container_width=True, key="btn_cover"):
        if not job_role.strip() or not company_name.strip():
            st.error("Please enter both the job role and company name.")
        else:
            result = call_groq(
                f"""Write a professional, compelling cover letter for:
- Job Role: {job_role}
- Company: {company_name}
- Candidate Resume: {text}

The letter should:
- Be 3-4 paragraphs
- Show genuine enthusiasm for the company
- Highlight the most relevant skills from the resume
- End with a strong call to action
- Sound human and personalized, not generic""",
                "Writing your cover letter..."
            )
            if result:
                st.success("Cover Letter Generated!")
                st.markdown(f"<div class='ai-output-card'>{result}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # =====================================
    # AI INTERVIEW QUESTIONS
    # =====================================

    st.markdown("<h3 style='color:white'>🎯 AI Interview Question Generator</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8'>Get personalized interview questions based on your resume.</p>", unsafe_allow_html=True)

    difficulty = st.select_slider(
        "Question Difficulty",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Intermediate",
        key="interview_difficulty"
    )

    if st.button("🎯 Generate Interview Questions", use_container_width=True, key="btn_interview"):
        result = call_groq(
            f"""Based on this resume, generate 10 {difficulty}-level interview questions.
Include a mix of:
- Technical questions (based on their skills)
- Behavioral questions (based on their experience)
- Project-based questions (based on their projects)

For each question, provide a brief expected answer hint.

Resume:
{text}""",
            "Generating interview questions..."
        )
        if result:
            st.success("Questions Ready!")
            st.markdown(f"<div class='ai-output-card'>{result}</div>", unsafe_allow_html=True)
