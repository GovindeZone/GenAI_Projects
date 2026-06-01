import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

from resume_parser import load_resumes
from ranking_engine import rank_candidates

# =========================================================
# LOAD API KEY
# =========================================================
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Job Application Management (JAM)",
    layout="wide"
)

# =========================================================
# INIT LLM (IMPORTANT FIX)
# =========================================================
@st.cache_resource
def get_llm():
    return ChatGroq(
        groq_api_key=groq_api_key,
        model="llama-3.1-8b-instant",
        temperature=0.3
    )

llm = get_llm()

# =========================================================
# CACHE RESUME LOADING (IMPORTANT FIX)
# =========================================================
@st.cache_data
def cached_load_resumes(folder):
    return load_resumes(folder)

# =========================================================
# EXPOSURE ANALYSIS FUNCTION (FIXED)
# =========================================================
def analyze_candidate_exposure(
    resume_text,
    job_role,
    required_skills,
    llm
):

    prompt = f"""
    You are an AI HR Recruitment Specialist.

    Analyze the resume deeply.

    JOB ROLE:
    {job_role}

    REQUIRED SKILLS:
    {required_skills}

    RESUME:
    {resume_text}

    Analyze:

    1. Real hands-on exposure
    2. Years of experience
    3. Project exposure
    4. Enterprise usage
    5. Skill depth
    6. Role suitability
    7. Domain fit

    Return:

    - Match Percentage
    - Experience Level
    - Strengths
    - Weaknesses
    - Final Recommendation

    Give professional HR evaluation.
    """

    response = llm.invoke(prompt)
    return response.content

# =========================================================
# SIDEBAR BANNER
# =========================================================
st.sidebar.markdown("""
<div style="
    background: linear-gradient(90deg, #1e3c72, #2a5298);
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 15px;
    text-align: center;
    width: 90%;
    margin-left: auto;
    margin-right: auto;
">

<h2 style="
    color: white;
    margin: 0;
    font-size: 20px;
    font-weight: 600;
">
🤖 Resume AI Engine
</h2>

<p style="
    color: #dfe9ff;
    margin-top: 6px;
    margin-bottom: 0px;
    font-size: 12px;
">
AI Powered Resume Analysis
</p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# UI HEADER
# =========================================================
st.markdown("""
<div style="
    background: linear-gradient(90deg, #1e3c72, #2a5298);
    padding: 16px 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.15);
">

<h1 style="color: white; margin: 0; font-size: 24px;">
Job Application Dashboard
</h1>

<p style="color: #dfe9ff; margin: 0; font-size: 14px;">
Candidate Fit Assessment (Skill Analysis & Ranking)
</p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR INPUTS
# =========================================================
st.sidebar.header("Job Requirement")

job_role = st.sidebar.text_input(
    "Enter Job Role",
    "Python Developer"
)

required_skills = st.sidebar.text_area(
    "Enter Required Skills",
    "Python, SQL, FastAPI, LangChain"
)

resume_folder = st.sidebar.text_input(
    "Resume Folder Path",
    "resumes"
)

# =========================================================
# EXPOSURE ANALYSIS
# =========================================================
if st.sidebar.button("🧠 Get Detailed Analysis"):

    try:
        st.subheader("🧠 AI Detailed Evaulation Report")

        resumes = cached_load_resumes(resume_folder)

        for resume in resumes:

            st.divider()
            st.markdown(f"## 📄 {resume['file_name']}")

            analysis = analyze_candidate_exposure(
                resume_text=resume["content"][:4000],  # performance safeguard
                job_role=job_role,
                required_skills=required_skills,
                llm=llm
            )

            st.write(analysis)

    except Exception as e:
        st.error(f"Exposure Analysis Error: {str(e)}")

# =========================================================
# START SCREENING
# =========================================================
if st.sidebar.button("🚀 Get Skill Matched Profile"):

    try:
        st.subheader("🧠 List of Skill Matched/Un-Matched Candidate")

        skills_list = [
            skill.strip().lower()
            for skill in required_skills.split(",")
        ]

        resumes = cached_load_resumes(resume_folder)

        results = rank_candidates(
            resumes,
            job_role,
            skills_list
        )

        df = pd.DataFrame(results)

        if df.empty:
            st.error("No resumes found.")
        else:

            df = df.sort_values(by="Match %", ascending=False)
            df.reset_index(drop=True, inplace=True)

            df.index = df.index + 1
            df.insert(0, "Rank", df.index)

            # Metrics
            total = len(df)
            matched = len(df[df["Match %"] >= 75])
            partial = len(df[(df["Match %"] >= 40) & (df["Match %"] < 75)])
            not_matched = len(df[df["Match %"] < 40])

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Resumes", total)
            col2.metric("Matched", matched)
            col3.metric("Partial Match", partial)
            col4.metric("Not Matched", not_matched)

            st.divider()

            st.dataframe(df, use_container_width=True, hide_index=True)

            # Export Excel
            os.makedirs("output", exist_ok=True)
            output_file = "output/shortlisted_candidates.xlsx"
            df.to_excel(output_file, index=False)

            with open(output_file, "rb") as f:
                st.download_button(
                    label="📥 Download Excel Report",
                    data=f,
                    file_name="Job_Application_Skill_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"Error: {str(e)}")