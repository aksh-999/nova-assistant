import sounddevice as sd
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel
import requests
import pyttsx3
from actions import handle_command

SAMPLE_RATE = 16000
RECORD_SECONDS = 5
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"

print("Loading Nova...")

whisper = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

print("Nova is ready!")
print("Press Ctrl+C to stop.\n")

while True:
    try:
        print("🎤 Listening...")

        audio = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16"
        )

        sd.wait()
        wav.write("voice.wav", SAMPLE_RATE, audio)

        segments, info = whisper.transcribe("voice.wav")

        user_text = "".join(
            segment.text for segment in segments
        ).strip()

        if not user_text:
            print("I couldn't hear you.\n")
            continue

        print("You:", user_text)

        # Check if the user gave Nova a computer command
        action_response = handle_command(user_text)

        if action_response:
            nova_response = action_response

        else:
            # Normal conversation goes to Ollama
            prompt = f"""
You are Nova, a personal voice assistant.

Be helpful, concise and natural.
Keep responses relatively short because you are speaking them aloud.

The user said:
{user_text}

Respond directly to the user.
"""

            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            response.raise_for_status()

            data = response.json()
            nova_response = data["response"].strip()

        print("Nova:", nova_response)

        # Speak response
        engine.say(nova_response)
        engine.runAndWait()

        print()

    except KeyboardInterrupt:
        print("\nNova stopped.")
        break

    except requests.exceptions.ConnectionError:
        print("❌ Can't connect to Ollama.")
        print("Make sure Ollama is running.\n")

    except Exception as e:
        print("❌ Error:", e)