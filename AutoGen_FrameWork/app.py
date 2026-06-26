import streamlit as st
import pandas as pd

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core import CancellationToken

from config import llm_config


# -----------------------------
# UI SETUP
# -----------------------------
st.set_page_config(page_title="AutoGen Business Report", layout="wide")

st.title("📊 AutoGen Business Report Generator")

uploaded_file = st.file_uploader("Upload Sales Data (Excel)", type=["xlsx"])


# -----------------------------
# LOAD DATA
# -----------------------------
if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("Preview Data")
    st.dataframe(df.head())


    if st.button("Generate Business Report"):

        # -----------------------------
        # AGENTS
        # -----------------------------

        analyst = AssistantAgent(
            name="Analyst",
            model_client_config=llm_config,
            system_message="You are a data analyst. Extract insights from sales data."
        )

        finance = AssistantAgent(
            name="Finance",
            model_client_config=llm_config,
            system_message="You are a finance expert. Validate revenue, margins, anomalies."
        )

        writer = AssistantAgent(
            name="Writer",
            model_client_config=llm_config,
            system_message="You are a business report writer. Write structured executive reports."
        )

        critic = AssistantAgent(
            name="Critic",
            model_client_config=llm_config,
            system_message="You review reports for clarity, accuracy, and business tone."
        )

        user = UserProxyAgent(
            name="User"
        )

        # -----------------------------
        # TEAM (FIXED PART)
        # -----------------------------

        team = RoundRobinGroupChat(
            participants=[user, analyst, finance, writer, critic]
        )

        # -----------------------------
        # PROMPT
        # -----------------------------

        prompt = f"""
You are given sales data.

Task:
1. Analyst → extract insights
2. Finance → validate numbers
3. Writer → create executive report
4. Critic → improve final report

DATA:
{df.to_string(index=False)}

Output:
A structured business report with:
- Summary
- Key insights
- Financial validation
- Risks
- Final recommendation
"""

        # -----------------------------
        # RUN (NEW STYLE)
        # -----------------------------

        result = team.run(task=prompt)

        st.subheader("📄 Final Report")
        st.write(result)