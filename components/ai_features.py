import streamlit as st
from groq import Groq

# =========================================
# AI FEATURES — Powered by Groq
# =========================================

def show_ai_features(api_key: str, text: str):
    """Display AI-powered resume features using Groq with full functionality"""
    
    # Header
    st.markdown("<h2 style='color:white'>🤖 AI Resume Features</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8'>Powered by Groq AI — Ultra fast inference</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Check if resume text exists
    if not text.strip():
        st.warning("⚠️ No resume text detected. Please upload a valid PDF.")
        return
    
    # Check if API key is configured
    if not api_key:
        st.error("⚠️ Groq API key not configured. Please add GROQ_API_KEY to secrets.")
        st.info("💡 Go to Settings → Secrets in Streamlit Cloud to add your API key.")
        return
    
    # Display API status
    st.success("✅ Groq API key is configured and ready")
    
    # =============================================
    # FEATURE 1: AI Resume Summary
    # =============================================
    st.markdown("### 📝 AI Resume Summary")
    st.markdown("Generates a professional ATS-optimized summary from your resume.")
    
    if st.button("Generate Resume Summary", key="gen_summary", use_container_width=True):
        prompt = f"""
        Generate a powerful, ATS-optimized professional summary (2-3 sentences) from this resume:
        
        {text[:4000]}
        
        Requirements:
        - Make it concise, impactful, and tailored for recruiters
        - Highlight key skills and achievements
        - Include relevant keywords for ATS
        - Keep it to 2-3 sentences maximum
        
        Output format: Just the summary, no additional text.
        """
        result = call_groq(api_key, prompt, "🧠 Generating professional summary...")
        if result:
            st.success("✅ Summary Generated Successfully!")
            st.markdown(
                f"""
                <div style="background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.3);
                            border-radius:12px;padding:20px;margin:10px 0;">
                    <p style="color:#e2e8f0;font-size:16px;line-height:1.6;">{result}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    
    # =============================================
    # FEATURE 2: AI Resume Feedback
    # =============================================
    st.markdown("### 💬 AI Resume Feedback")
    st.markdown("Get detailed, actionable feedback to improve your resume.")
    
    if st.button("Analyze & Get Feedback", key="get_feedback", use_container_width=True):
        prompt = f"""
        Provide detailed, actionable feedback on this resume:
        
        {text[:4000]}
        
        Please analyze and provide feedback on:
        1. **Strengths** - What's working well in this resume
        2. **Weaknesses** - What needs improvement
        3. **Missing Keywords** - Important keywords/skills that should be added
        4. **Formatting & Structure** - Suggestions for better layout
        5. **ATS Optimization** - Tips to improve ATS compatibility
        6. **Actionable Tips** - 3-5 specific things to change
        
        Format your response with clear headings for each section.
        Be specific, constructive, and actionable.
        """
        result = call_groq(api_key, prompt, "🧠 Analyzing your resume...")
        if result:
            st.success("✅ Feedback Generated Successfully!")
            st.markdown(
                f"""
                <div style="background:rgba(192,132,252,0.1);border:1px solid rgba(192,132,252,0.3);
                            border-radius:12px;padding:20px;margin:10px 0;">
                    <div style="color:#e2e8f0;font-size:15px;line-height:1.8;">{result}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    
    # =============================================
    # FEATURE 3: AI Skills Analysis
    # =============================================
    st.markdown("### 🎯 AI Skills Analysis")
    st.markdown("Identify key skills and gaps in your resume.")
    
    if st.button("Analyze Skills", key="analyze_skills", use_container_width=True):
        prompt = f"""
        Analyze the skills in this resume:
        
        {text[:4000]}
        
        Provide:
        1. **Top 10 Skills Detected** - List the most prominent skills
        2. **Missing In-Demand Skills** - Important skills not found
        3. **Skill Category Breakdown** - Technical vs Soft Skills
        4. **Recommendations** - Which skills to add or highlight
        
        Be specific and practical.
        """
        result = call_groq(api_key, prompt, "🧠 Analyzing your skills...")
        if result:
            st.success("✅ Skills Analysis Complete!")
            st.markdown(
                f"""
                <div style="background:rgba(74,222,128,0.1);border:1px solid rgba(74,222,128,0.3);
                            border-radius:12px;padding:20px;margin:10px 0;">
                    <div style="color:#e2e8f0;font-size:15px;line-height:1.8;">{result}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    
    # =============================================
    # FEATURE 4: AI Cover Letter Generator
    # =============================================
    st.markdown("### ✉️ AI Cover Letter Generator")
    st.markdown("Generate a tailored cover letter for any job.")
    
    col1, col2 = st.columns(2)
    with col1:
        job_role = st.text_input("Job Role", placeholder="e.g. Machine Learning Engineer", key="cover_role")
    with col2:
        company_name = st.text_input("Company Name", placeholder="e.g. Google", key="cover_company")
    
    if st.button("✉️ Generate Cover Letter", use_container_width=True, key="btn_cover"):
        if not job_role.strip() or not company_name.strip():
            st.error("⚠️ Please enter both the job role and company name.")
        else:
            prompt = f"""
            Write a professional, compelling cover letter for:
            - Job Role: {job_role}
            - Company: {company_name}
            - Candidate Resume: {text[:3000]}
            
            The letter should:
            - Be 3-4 paragraphs
            - Show genuine enthusiasm for the company
            - Highlight the most relevant skills from the resume
            - End with a strong call to action
            - Sound human and personalized, not generic
            """
            result = call_groq(api_key, prompt, "✉️ Writing your cover letter...")
            if result:
                st.success("✅ Cover Letter Generated!")
                st.markdown(
                    f"""
                    <div style="background:rgba(251,191,36,0.1);border:1px solid rgba(251,191,36,0.3);
                                border-radius:12px;padding:20px;margin:10px 0;">
                        <div style="color:#e2e8f0;font-size:15px;line-height:1.8;white-space:pre-wrap;">{result}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    st.markdown("---")
    
    # =============================================
    # FEATURE 5: AI Interview Questions
    # =============================================
    st.markdown("### 🎯 AI Interview Question Generator")
    st.markdown("Get personalized interview questions based on your resume.")
    
    difficulty = st.select_slider(
        "Question Difficulty",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Intermediate",
        key="interview_difficulty"
    )
    
    if st.button("🎯 Generate Interview Questions", use_container_width=True, key="btn_interview"):
        prompt = f"""
        Based on this resume, generate 10 {difficulty}-level interview questions.
        
        Resume:
        {text[:4000]}
        
        Include a mix of:
        - Technical questions (based on their skills)
        - Behavioral questions (based on their experience)
        - Project-based questions (based on their projects)
        
        For each question, provide a brief expected answer hint.
        Format: Number each question clearly.
        """
        result = call_groq(api_key, prompt, "🎯 Generating interview questions...")
        if result:
            st.success("✅ Questions Ready!")
            st.markdown(
                f"""
                <div style="background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.3);
                            border-radius:12px;padding:20px;margin:10px 0;">
                    <div style="color:#e2e8f0;font-size:15px;line-height:1.8;white-space:pre-wrap;">{result}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    
    # =============================================
    # API Status Footer
    # =============================================
    st.markdown("### 📡 API Status")
    col_status1, col_status2, col_status3 = st.columns(3)
    with col_status1:
        st.markdown(
            """
            <div style="background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.3);
                        border-radius:8px;padding:10px;text-align:center;">
                <div style="color:#22c55e;font-size:12px;">✅ API Key</div>
                <div style="color:#94a3b8;font-size:11px;">Configured</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_status2:
        st.markdown(
            """
            <div style="background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.3);
                        border-radius:8px;padding:10px;text-align:center;">
                <div style="color:#38bdf8;font-size:12px;">🔄 Model</div>
                <div style="color:#94a3b8;font-size:11px;">Llama 3.3 70B</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_status3:
        st.markdown(
            """
            <div style="background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.3);
                        border-radius:8px;padding:10px;text-align:center;">
                <div style="color:#a855f7;font-size:12px;">📊 Status</div>
                <div style="color:#94a3b8;font-size:11px;">Ready</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================
# HELPER FUNCTION: Call Groq API
# =========================================

def call_groq(api_key: str, prompt: str, spinner_msg: str) -> str:
    """
    Call Groq API with error handling and timeout.
    
    Args:
        api_key (str): Groq API key
        prompt (str): The prompt to send to the model
        spinner_msg (str): Message to show while loading
    
    Returns:
        str: The model's response or None if error
    """
    try:
        with st.spinner(spinner_msg):
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert resume analyst, career coach, and professional writer. Provide detailed, actionable, and professional responses."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1024,
                timeout=30.0
            )
            return response.choices[0].message.content
    except Exception as e:
        st.error(f"❌ Groq API error: {str(e)}")
        st.info("💡 Troubleshooting tips:\n- Check your API key is valid\n- Ensure you have credits available\n- Try again in a few seconds")
        return None
