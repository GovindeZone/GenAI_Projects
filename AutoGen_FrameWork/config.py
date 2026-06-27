import os
from dotenv import load_dotenv

# IMPORTANT: force load .env from current folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
BASE_URL = os.getenv("BASE_URL", "https://api.groq.com/openai/v1")

TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))

# DEBUG (temporary)
print("ENV LOADED:", GROQ_API_KEY is not None)

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")