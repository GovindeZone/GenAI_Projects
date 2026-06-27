from autogen_agentchat.agents import AssistantAgent

from utils.model_client import model_client


def create_analyst():

    return AssistantAgent(
        name="Analyst",

        model_client=model_client,

        system_message="""
You are an experienced Senior Business Data Analyst.

Responsibilities

- Analyze uploaded sales data.

- Identify trends.

- Find top-performing products.

- Find worst-performing products.

- Detect anomalies.

- Identify seasonal patterns.

- Explain business impact.

Never create fictional numbers.

Only use information available in the dataset.
"""
    )