import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")
    apify_key = os.getenv("APIFY_API_KEY")

    if not openai_key:
        raise ValueError("OPENAI_API_KEY is not set.")
    if not apify_key:
        raise ValueError("APIFY_API_KEY is not set.")

    return openai_key, apify_key
