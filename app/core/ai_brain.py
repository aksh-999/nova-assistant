import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY was not found. Check your .env file."
    )


client = genai.Client(api_key=api_key)


def ask_gemini(user_text):
    prompt = f"""
You are Nova, a personal AI voice assistant.

Be helpful, natural and concise.
The response will be spoken aloud, so keep it reasonably short.

User:
{user_text}

Respond directly.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        if not response.text:
            return "I didn't get a response from Gemini."

        return response.text.strip()

    except Exception as e:
        error_text = str(e)

        if "503" in error_text or "UNAVAILABLE" in error_text:
            return (
                "Gemini is temporarily busy right now. "
                "Please try again in a moment."
            )

        return f"Gemini error: {error_text}"    