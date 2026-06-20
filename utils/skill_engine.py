# =========================================
# DETECT RESUME SKILLS
# =========================================

def detect_skills(

    resume_text,

    skills_list
):

    detected_skills = []

    for skill in skills_list:

        if skill.lower() in resume_text:

            detected_skills.append(skill)

    return list(set(detected_skills))

# =========================================
# DETECT JOB DESCRIPTION SKILLS
# =========================================

def detect_job_skills(

    job_description,

    skills_list
):

    job_skills = []

    for skill in skills_list:

        if skill.lower() in job_description:

            job_skills.append(skill)

    return list(set(job_skills))

# =========================================
# CALCULATE ATS SCORE
# =========================================

def calculate_ats_score(

    detected_skills,

    required_skills
):

    matched_skills = 0

    for skill in required_skills:

        if skill in detected_skills:

            matched_skills += 1

    ats_score = (

        matched_skills
        / len(required_skills)

    ) * 100

    return ats_score

# =========================================
# CALCULATE JOB MATCH SCORE
# =========================================

def calculate_job_match(

    detected_skills,

    job_skills
):

    matched_job_skills = []

    for skill in job_skills:

        if skill in detected_skills:

            matched_job_skills.append(skill)

    if len(job_skills) > 0:

        job_match_score = (

            len(matched_job_skills)
            / len(job_skills)

        ) * 100

    else:

        job_match_score = 0

    return (

        job_match_score,

        matched_job_skills
    )

# =========================================
# CALCULATE RESUME STRENGTH
# =========================================

def calculate_resume_strength(

    ats_score,

    job_match_score,

    detected_skills
):

    strength_score = 0

    strength_score += ats_score * 0.4

    strength_score += job_match_score * 0.4

    skill_bonus = min(

        len(detected_skills) * 2,

        20
    )

    strength_score += skill_bonus

    strength_score = min(

        round(strength_score),

        100
    )

    return (

        strength_score,

        skill_bonus
    )

# =========================================
# DETECT RESUME CATEGORY
# =========================================

def detect_resume_category(

    resume_text
):

    resume_category = "General Resume"

    if (

        "machine learning" in resume_text
        or
        "deep learning" in resume_text

    ):

        resume_category = "AI/ML Engineer"

    elif (

        "react" in resume_text
        or
        "javascript" in resume_text

    ):

        resume_category = "Web Developer"

    elif (

        "aws" in resume_text
        or
        "docker" in resume_text

    ):

        resume_category = "Cloud Engineer"

    elif (

        "data science" in resume_text

    ):

        resume_category = "Data Scientist"

    return resume_category
