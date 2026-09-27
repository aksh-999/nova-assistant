import sys
import sounddevice as sd
import scipy.io.wavfile as wav
import requests
import pyttsx3

from faster_whisper import WhisperModel
from actions import handle_command
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt, QThread, Signal


SAMPLE_RATE = 16000
RECORD_SECONDS = 5

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"


# ============================================================
# NOVA VOICE WORKER
# ============================================================

class NovaWorker(QThread):

    finished = Signal(str)
    error = Signal(str)

    def run(self):

        try:
            # -------------------------
            # Record audio
            # -------------------------

            audio = sd.rec(
                int(RECORD_SECONDS * SAMPLE_RATE),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="int16"
            )

            sd.wait()

            wav.write(
                "voice.wav",
                SAMPLE_RATE,
                audio
            )

            # -------------------------
            # Whisper
            # -------------------------

            whisper = WhisperModel(
                "base",
                device="cpu",
                compute_type="int8"
            )

            segments, info = whisper.transcribe(
                "voice.wav"
            )

            user_text = "".join(
                segment.text for segment in segments
            ).strip()

            if not user_text:
                self.finished.emit(
                    "I couldn't hear you."
                )
                return

            # -------------------------
            # Ollama
            # -------------------------

            prompt = f"""
You are Nova, a personal AI assistant.

Be helpful, concise and natural.

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

            # -------------------------
            # Voice
            # -------------------------

            engine = pyttsx3.init()

            engine.setProperty(
                "rate",
                175
            )

            engine.setProperty(
                "volume",
                1.0
            )

            engine.say(nova_response)

            engine.runAndWait()

            engine.stop()

            self.finished.emit(
                f"You: {user_text}\n\nNova: {nova_response}"
            )

        except Exception as e:

            self.error.emit(
                str(e)
            )


# ============================================================
# NOVA APPLICATION
# ============================================================

class NovaApp(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Nova")

        self.setFixedSize(
            420,
            520
        )

        self.setStyleSheet("""
            QWidget {
                background-color: #0b0b0f;
                color: white;
                font-family: Arial;
            }

            QLabel#logo {
                font-size: 48px;
            }

            QLabel#title {
                font-size: 32px;
                font-weight: bold;
            }

            QLabel#status {
                color: #999999;
                font-size: 15px;
            }

            QLabel#response {
                color: #dddddd;
                font-size: 14px;
            }

            QPushButton {
                background-color: white;
                color: black;
                border: none;
                border-radius: 45px;
                font-size: 18px;
                font-weight: bold;
                min-width: 150px;
                min-height: 90px;
            }

            QPushButton:hover {
                background-color: #dddddd;
            }

            QPushButton:pressed {
                background-color: #bbbbbb;
            }

            QPushButton:disabled {
                background-color: #555555;
                color: #aaaaaa;
            }
        """)

        layout = QVBoxLayout()

        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.setSpacing(15)

        # -------------------------
        # Logo
        # -------------------------

        logo = QLabel("✦")

        logo.setObjectName(
            "logo"
        )

        logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # -------------------------
        # Name
        # -------------------------

        title = QLabel("Nova")

        title.setObjectName(
            "title"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # -------------------------
        # Status
        # -------------------------

        status = QLabel(
            "Your personal AI assistant"
        )

        status.setObjectName(
            "status"
        )

        status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.status = status

        # -------------------------
        # Response
        # -------------------------

        response = QLabel("")

        response.setObjectName(
            "response"
        )

        response.setWordWrap(
            True
        )

        response.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.response = response

        # -------------------------
        # Button
        # -------------------------

        self.talk_button = QPushButton(
            "🎙  TALK"
        )

        self.talk_button.clicked.connect(
            self.start_listening
        )

        # -------------------------
        # Layout
        # -------------------------

        layout.addWidget(
            logo
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            status
        )

        layout.addSpacing(
            15
        )

        layout.addWidget(
            response
        )

        layout.addSpacing(
            20
        )

        layout.addWidget(
            self.talk_button,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.setLayout(
            layout
        )

        self.worker = None


    # ========================================================
    # START LISTENING
    # ========================================================

    def start_listening(self):

        self.status.setText(
            "Listening..."
        )

        self.talk_button.setText(
            "🎙  LISTENING"
        )

        self.talk_button.setEnabled(
            False
        )

        self.response.setText(
            ""
        )

        self.worker = NovaWorker()

        self.worker.finished.connect(
            self.nova_finished
        )

        self.worker.error.connect(
            self.nova_error
        )

        self.worker.start()


    # ========================================================
    # FINISHED
    # ========================================================

    def nova_finished(
        self,
        result
    ):

        self.status.setText(
            "Ready"
        )

        self.talk_button.setText(
            "🎙  TALK"
        )

        self.talk_button.setEnabled(
            True
        )

        self.response.setText(
            result
        )


    # ========================================================
    # ERROR
    # ========================================================

    def nova_error(
        self,
        error
    ):

        self.status.setText(
            "Something went wrong"
        )

        self.talk_button.setText(
            "🎙  TALK"
        )

        self.talk_button.setEnabled(
            True
        )

        self.response.setText(
            error
        )


# ============================================================
# START APP
# ============================================================

app = QApplication(
    sys.argv
)

window = NovaApp()

window.show()

sys.exit(
    app.exec()
)