from autogen_agentchat.agents import AssistantAgent

from utils.model_client import model_client


def create_critic():

    return AssistantAgent(

        name="Critic",

        model_client=model_client,

        system_message="""
You are a Senior Business Consultant.

Review reports for

• Accuracy

• Clarity

• Completeness

• Business tone

If improvements are needed,

provide constructive feedback.

Otherwise approve the report.
"""
    )