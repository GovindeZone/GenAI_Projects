from autogen_ext.models.openai import OpenAIChatCompletionClient

from config import (
    GROQ_API_KEY,
    MODEL_NAME,
    BASE_URL,
)

# IMPORTANT: model metadata for non-OpenAI models (Groq, etc.)
model_info = {
    "vision": False,
    "function_calling": False,
    "json_output": False,
    "family": "llama",
}

model_client = OpenAIChatCompletionClient(
    model=MODEL_NAME,
    api_key=GROQ_API_KEY,
    base_url=BASE_URL,
    model_info=model_info
)