"""
GEN AI APPLICATION:
AI Love Quote Generator ❤️
"""

# =========================================================
# IMPORTS
# =========================================================

import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from pydantic import BaseModel, Field


# =========================================================
# LOAD ENV VARIABLES
# =========================================================

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    print("WARNING: GROQ_API_KEY not found")


# =========================================================
# MODEL (LLM)
# =========================================================

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model="llama-3.1-8b-instant",
    temperature=0.9,
    timeout=30
)


# =========================================================
# OUTPUT PARSER
# =========================================================

class LoveQuotes(BaseModel):
    quote_1: str = Field(description="First romantic love quote")
    quote_2: str = Field(description="Second romantic love quote")


parser = JsonOutputParser(
    pydantic_object=LoveQuotes
)


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_template(
    """
You are a romantic AI assistant.

Return ONLY valid JSON.
Do not add explanation or extra text.

The user's lover name is:
{lover_name}

The flower is:
{flower_name}

The favorite food is:
{food_name}

Generate:
1. Two romantic love quotes
2. Blend all three elements naturally
3. Keep them short

{format_instructions}
"""
)


# =========================================================
# CHAIN
# =========================================================

chain = prompt | llm | parser


# =========================================================
# MAIN FUNCTION
# =========================================================

def generate_love_quotes(lover_name: str, flower_name: str, food_name: str):

    try:
        response = chain.invoke({
            "lover_name": lover_name,
            "flower_name": flower_name,
            "food_name": food_name,
            "format_instructions": parser.get_format_instructions()
        })

        return response

    except Exception as e:
        return {
            "quote_1": "Error generating quote",
            "quote_2": str(e)
        }


# =========================================================
# TEST RUN
# =========================================================

if __name__ == "__main__":

    result = generate_love_quotes(
        lover_name="Sophia",
        flower_name="Rose",
        food_name="Chocolate Cake"
    )

    print("\n========== LOVE QUOTES ==========\n")

    print("Quote 1:")
    print(result.get("quote_1"))

    print("\nQuote 2:")
    print(result.get("quote_2"))