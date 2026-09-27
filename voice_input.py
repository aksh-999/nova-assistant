import sounddevice as sd
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
RECORD_SECONDS = 5

print("Loading Nova's speech recognition...")
model = WhisperModel("base", device="cpu", compute_type="int8")

print("\nNova is ready.")
print("Speak for 5 seconds...\n")

audio = sd.rec(
    int(RECORD_SECONDS * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16"
)

sd.wait()

wav.write("voice.wav", SAMPLE_RATE, audio)

segments, info = model.transcribe("voice.wav")

text = "".join(segment.text for segment in segments).strip()

print("You said:")
print(text)