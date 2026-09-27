import sounddevice as sd
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel


SAMPLE_RATE = 16000
RECORD_SECONDS = 5
AUDIO_FILE = "voice.wav"


class SpeechToText:
    def __init__(self):
        print("Loading Whisper...")

        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

        print("Whisper ready!")

    def listen(self):
        print("🎤 Listening...")

        audio = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        wav.write(
            AUDIO_FILE,
            SAMPLE_RATE,
            audio
        )

        segments, info = self.model.transcribe(
            AUDIO_FILE,
            language="en"
        )

        text = "".join(
            segment.text for segment in segments
        ).strip()

        return text