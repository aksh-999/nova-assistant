import os

import requests
from dotenv import load_dotenv
from google import genai


load_dotenv()


# ============================================================
# GEMINI SETUP
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

gemini_client = None

if api_key:
    gemini_client = genai.Client(
        api_key=api_key,
        http_options={
            "timeout": 10000
        }
    )


# ============================================================
# CONFIGURATION
# ============================================================

GEMINI_MODEL = "gemini-3.8-flash"

OLLAMA_MODEL = "llama3.2:3b"

OLLAMA_URL = "http://localhost:11434/api/generate"


# ============================================================
# SHARED NOVA PROMPT
# ============================================================

def build_prompt(user_text):
    return f"""
You are Nova, a personal AI voice assistant.

You are running on the user's computer.

Be helpful, natural, concise and practical.
The response may be spoken aloud, so avoid unnecessary long explanations.

User:
{user_text}

Respond directly to the user.
"""


# ============================================================
# GEMINI
# ============================================================

def ask_gemini(user_text):
    """
    Ask Gemini for a response.

    Returns:
        str | None

    Returns None if Gemini is unavailable,
    times out, or encounters an error.
    """

    if gemini_client is None:
        print("[Gemini] API key not available.")
        return None

    prompt = build_prompt(user_text)

    try:
        print("[Nova AI] Trying Gemini...")

        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if not response.text:
            print("[Gemini] Empty response.")
            return None

        return response.text.strip()

    except Exception as e:
        print(f"[Gemini unavailable] {e}")
        return None


# ============================================================
# OLLAMA
# ============================================================

def ask_ollama(user_text):
    """
    Ask the local Ollama model for a response.

    Returns:
        str | None

    Returns None if Ollama is unavailable.
    """

    prompt = build_prompt(user_text)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        print("[Nova AI] Trying local Ollama...")

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        result = data.get("response")

        if not result:
            print("[Ollama] Empty response.")
            return None

        return result.strip()

    except Exception as e:
        print(f"[Ollama unavailable] {e}")
        return None


# ============================================================
# MAIN AI ROUTER
# ============================================================

def ask_ai(user_text):
    """
    Nova's main AI entry point.

    Priority:

        1. Gemini
        2. Ollama
        3. Friendly fallback message
    """

    # --------------------------------------------------------
    # 1. Try Gemini
    # --------------------------------------------------------

    gemini_response = ask_gemini(user_text)

    if gemini_response:
        print("[Nova AI] Using Gemini")
        return gemini_response

    # --------------------------------------------------------
    # 2. Gemini failed → Ollama
    # --------------------------------------------------------

    print("[Nova AI] Gemini unavailable. Switching to Ollama...")

    ollama_response = ask_ollama(user_text)

    if ollama_response:
        print("[Nova AI] Using Ollama")
        return ollama_response

    # --------------------------------------------------------
    # 3. Both failed
    # --------------------------------------------------------

    return (
        "I'm having trouble connecting to my AI systems right now. "
        "Please make sure Ollama is running and try again."
    )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def ask_gemini_with_fallback(user_text):
    """
    Backward-compatible function name.
    """

    return ask_ai(user_text)    