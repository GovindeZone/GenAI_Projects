from autogen_agentchat.agents import AssistantAgent

from utils.model_client import model_client


def create_finance():

    return AssistantAgent(

        name="Finance",

        model_client=model_client,

        system_message="""
You are a Chartered Financial Analyst.

Responsibilities

Validate

• Revenue

• Profit

• Margin

• Growth

Identify

• Financial risks

• Revenue leakage

• High-cost products

• Negative margins

Explain financial implications.

Never invent financial values.
"""
    )