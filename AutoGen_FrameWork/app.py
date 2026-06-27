import asyncio
import os

import streamlit as st

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination

from agents import (
    create_analyst,
    create_finance,
)

from utils.excel_reader import load_excel
from utils.report_export import export_docx


# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="AI Business Report Generator",
    layout="wide"
)

st.title("📊 AI Multi-Agent Business Report Generator")


# ----------------------------------
# HELPER FUNCTIONS
# ----------------------------------

def clean_report_text(text: str) -> str:
    """
    Clean LLM output to avoid Streamlit markdown/math formatting issues.
    """

    if not text:
        return ""

    text = text.replace("\\(", "")
    text = text.replace("\\)", "")
    text = text.replace("\\[", "")
    text = text.replace("\\]", "")
    text = text.replace("$", "USD ")

    return text


def make_small_summary(df):
    """
    Creates small input for Groq token limits.
    """

    df_small = df.copy()

    # Limit columns and rows
    df_small = df_small.iloc[:, :8]
    df_small = df_small.head(5)

    # Limit long text inside cells
    for col in df_small.columns:
        df_small[col] = df_small[col].astype(str).str.slice(0, 40)

    sample_data = df_small.to_csv(index=False)

    numeric_summary = df.describe(include="number").round(2)

    if not numeric_summary.empty:
        numeric_text = numeric_summary.to_string()
    else:
        numeric_text = "No numeric columns available."

    summary = f"""
Rows: {len(df)}
Columns: {len(df.columns)}
Column Names: {", ".join(df.columns[:8])}

Sample Data:
{sample_data}

Numeric Summary:
{numeric_text}
"""

    return summary


# ----------------------------------
# FILE UPLOAD
# ----------------------------------

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file:

    df = load_excel(uploaded_file)

    st.subheader("Preview")
    st.dataframe(df.head())

    st.write(f"Rows: {len(df)}")
    st.write(f"Columns: {len(df.columns)}")

    if st.button("Generate Business Report"):

        summary_text = make_small_summary(df)

        analyst = create_analyst()
        finance = create_finance()

        termination = MaxMessageTermination(max_messages=3)

        team = RoundRobinGroupChat(
            participants=[
                analyst,
                finance,
            ],
            termination_condition=termination
        )

        prompt = f"""
Use the business sales data summary below and create a concise business report.

IMPORTANT RULES:
- Do not use LaTeX.
- Do not use mathematical notation.
- Do not use formulas.
- Do not use dollar symbols.
- Use USD instead of dollar symbols.
- Write plain business English only.
- Keep the response concise.

DATA SUMMARY:
{summary_text}

TASK FLOW:

Analyst:
- Give 3 key insights.
- Identify important trends.

Finance:
- Give 3 financial observations.
- Identify risks or anomalies.

FINAL OUTPUT FORMAT:

# Executive Summary

# Key Insights

# Financial Observations

# Risks

# Recommendations
"""

        async def run_team():
            return await team.run(task=prompt)

        try:
            with st.spinner("AI Agents are collaborating..."):
                result = asyncio.run(run_team())

            final_report = result.messages[-1].content
            final_report = clean_report_text(final_report)

            st.success("Business Report Generated")
            st.markdown(final_report)

            os.makedirs("output/reports", exist_ok=True)

            output_file = "output/reports/Business_Report.docx"

            export_docx(final_report, output_file)

            with open(output_file, "rb") as file:
                st.download_button(
                    label="Download DOCX",
                    data=file,
                    file_name="Business_Report.docx"
                )

        except Exception as e:
            st.error("Report generation failed.")
            st.write(str(e))