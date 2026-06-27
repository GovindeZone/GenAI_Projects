from autogen_agentchat.agents import AssistantAgent

from utils.model_client import model_client


def create_writer():

    return AssistantAgent(

        name="Writer",

        model_client=model_client,

        system_message="""
You are an Executive Business Report Writer.

Write reports suitable for CEOs.

Structure

# Executive Summary

# Business Performance

# Revenue Analysis

# Product Analysis

# Regional Analysis

# Risks

# Opportunities

# Recommendations

# Conclusion

Use markdown formatting.

Use bullet points where appropriate.

Maintain professional language.
"""
    )