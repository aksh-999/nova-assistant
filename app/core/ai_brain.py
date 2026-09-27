import os

import requests
from dotenv import load_dotenv
from google import genai


load_dotenv()


# ============================================================
# AI CONFIGURATION
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


GEMINI_MODEL = "gemini-3.8-flash"

OLLAMA_MODEL = "llama3.2:3b"

OLLAMA_URL = "http://localhost:11434/api/generate"


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_prompt(user_text, memory_context=None):

    memory_section = ""

    if memory_context:
        memory_section = f"""
Relevant memories about the user:

{memory_context}

Use these memories when they are relevant.
Do not mention the memory system unless the user asks about it.
Do not invent information that is not present in the memories.
"""

    return f"""
You are Nova, a personal AI voice assistant.

You are running on the user's computer.

Be helpful, natural, concise and practical.
The response may be spoken aloud, so avoid unnecessary long explanations.

{memory_section}

User:
{user_text}

Respond directly to the user.
"""


# ============================================================
# GEMINI
# ============================================================

def ask_gemini(user_text, memory_context=None):

    if gemini_client is None:
        print("[Gemini] API key not available.")
        return None

    prompt = build_prompt(
        user_text,
        memory_context
    )

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

def ask_ollama(user_text, memory_context=None):

    prompt = build_prompt(
        user_text,
        memory_context
    )

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
# MAIN AI FUNCTION
# ============================================================

def ask_ai(user_text, memory_context=None):

    gemini_response = ask_gemini(
        user_text,
        memory_context
    )

    if gemini_response:

        print("[Nova AI] Using Gemini")

        return gemini_response


    print(
        "[Nova AI] Gemini unavailable. "
        "Switching to Ollama..."
    )


    ollama_response = ask_ollama(
        user_text,
        memory_context
    )

    if ollama_response:

        print("[Nova AI] Using Ollama")

        return ollama_response


    return (
        "I'm having trouble connecting to my AI systems right now. "
        "Please make sure Ollama is running and try again."
    )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def ask_gemini_with_fallback(
    user_text,
    memory_context=None
):

    return ask_ai(
        user_text,
        memory_context
    )