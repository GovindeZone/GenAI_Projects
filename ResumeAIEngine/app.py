import streamlit as st
import pandas as pd
import os

from resume_parser import load_resumes
from ranking_engine import rank_candidates


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Job Application Management (JAM)",
    layout="wide"
)

# =========================================================
# TOP HEADER
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

<h1 style="
    color: white;
    margin: 0;
    font-size: 24px;
    font-weight: 600;
">
Job Application Dashboard
</h1>

<p style="
    color: #dfe9ff;
    margin-top: 6px;
    margin-bottom: 0px;
    font-size: 14px;
">
Candidate Skill Analysis & Ranking
</p>

</div>
""", unsafe_allow_html=True)


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
# START SCREENING
# =========================================================

if st.sidebar.button("🚀 Start Screening"):

    try:

        skills_list = [
            skill.strip().lower()
            for skill in required_skills.split(",")
        ]

        resumes = load_resumes(resume_folder)

        results = rank_candidates(
            resumes,
            job_role,
            skills_list
        )

        # =========================================
# CREATE DATAFRAME
# =========================================

        # =========================================
        # CREATE DATAFRAME
        # =========================================

        df = pd.DataFrame(results)

        # =========================================
        # EMPTY CHECK
        # =========================================

        if df.empty:

            st.error("No resumes found.")

        else:

            # =========================================
            # SORT DATA
            # =========================================

            df = df.sort_values(
                by="Match %",
                ascending=False
            )

            # =========================================
            # RESET INDEX
            # =========================================

            df.reset_index(
                drop=True,
                inplace=True
            )

            # =========================================
            # ADD RANK COLUMN
            # =========================================

            df.index = df.index + 1

            df.insert(
                0,
                "Rank",
                df.index
            )

            # =========================================
            # METRICS
            # =========================================

            total = len(df)

            matched = len(
                df[df["Match %"] >= 75]
            )

            partial = len(
                df[
                    (df["Match %"] >= 40)
                    & (df["Match %"] < 75)
                ]
            )

            not_matched = len(
                df[df["Match %"] < 40]
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Total Resumes",
                total
            )

            col2.metric(
                "Matched",
                matched
            )

            col3.metric(
                "Partial Match",
                partial
            )

            col4.metric(
                "Not Matched",
                not_matched
            )

            st.divider()

            # =========================================
            # TABLE
            # =========================================

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # =========================================
            # EXPORT EXCEL
            # =========================================

            os.makedirs(
                "output",
                exist_ok=True
            )

            output_file = (
                "output/shortlisted_candidates.xlsx"
            )

            df.to_excel(
                output_file,
                index=False
            )

            with open(output_file, "rb") as f:

                st.download_button(
                    label="📥 Download Excel Report",
                    data=f,
                    file_name="shortlisted_candidates.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:

        st.error(f"Error: {str(e)}")