import asyncio

import streamlit as st

from autogen_agentchat.teams import RoundRobinGroupChat

from agents import (
    create_analyst,
    create_finance,
    create_writer,
    create_critic
)

from utils.excel_reader import load_excel
from utils.helper import dataframe_summary
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

    st.write(f"Rows : {len(df)}")

    st.write(f"Columns : {len(df.columns)}")

    if st.button("Generate Business Report"):

        # ----------------------------
        # LIMIT DATA (VERY IMPORTANT)
        # ----------------------------
        df_small = df.head(15)   # reduced from 20 → safer for Groq
        summary_text = df_small.to_string(index=False)

        analyst = create_analyst()
        finance = create_finance()
        #writer = create_writer()
        #critic = create_critic()

        team = RoundRobinGroupChat(
            participants=[
                analyst,
                finance,
                #writer,
                #critic
            ]
        )

        # ----------------------------
        # OPTIMIZED PROMPT (LOW TOKENS)
        # ----------------------------
        prompt = f"""
    Business Sales Data (sample only):

    {summary_text}

    TASK FLOW:

    Analyst:
    - key insights
    - trends

    Finance:
    - revenue validation
    - anomalies

    Writer:
    - executive report

    Critic:
    - review clarity and correctness

    Final Output: structured business report
    """

        async def run_team():
            try:
                result = await team.run(task=prompt)
                return result
            except Exception as e:
                return str(e)

        with st.spinner("AI Agents are collaborating..."):

            result = asyncio.run(run_team())

        # ----------------------------
        # SAFE OUTPUT HANDLING
        # ----------------------------
        if isinstance(result, str):
            st.error(result)
        else:
            final_report = result.messages[-1].content

            st.success("Business Report Generated")

            st.markdown(final_report)

            output_file = "output/reports/Business_Report.docx"

            export_docx(final_report, output_file)

            with open(output_file, "rb") as file:
                st.download_button(
                    label="Download DOCX",
                    data=file,
                    file_name="Business_Report.docx"
                )