import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def query_openrouter(resume_text, job_text):
    """
    Calls OpenRouter's unified API with resume and job description to get analysis.
    """
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Analyze the following resume and job description.
Return:
- A match score (0–100)
- Missing skills or keywords
- some improved bullet points rewritten or missing from the resume

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_text}
"""

    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        result = response.json()
        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ API call failed: {e}"
