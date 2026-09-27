import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt, QThread, Signal

from app.voice.speech_to_text import SpeechToText
from app.voice.text_to_speech import TextToSpeech
from app.core.assistant import NovaAssistant


class NovaWorker(QThread):
    finished = Signal(str)
    error = Signal(str)

    def run(self):
        try:
            stt = SpeechToText()
            tts = TextToSpeech()
            assistant = NovaAssistant()

            # Listen
            user_text = stt.listen()

            if not user_text:
                self.finished.emit("I couldn't hear you.")
                assistant.close()
                return

            # Process
            nova_response = assistant.process(user_text)

            # Speak
            tts.speak(nova_response)

            self.finished.emit(
                f"You: {user_text}\n\nNova: {nova_response}"
            )

            assistant.close()
            tts.stop()

        except Exception as e:
            self.error.emit(str(e))


class NovaApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nova")
        self.setFixedSize(420, 520)

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
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        logo = QLabel("✦")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Nova")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        status = QLabel("Your personal AI assistant")
        status.setObjectName("status")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status = status

        response = QLabel("")
        response.setObjectName("response")
        response.setWordWrap(True)
        response.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.response = response

        self.talk_button = QPushButton("🎙  TALK")
        self.talk_button.clicked.connect(self.start_listening)

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(status)

        layout.addSpacing(15)

        layout.addWidget(response)

        layout.addSpacing(20)

        layout.addWidget(
            self.talk_button,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.setLayout(layout)

        self.worker = None

    def start_listening(self):

        self.status.setText("Listening...")
        self.talk_button.setText("🎙  LISTENING")
        self.talk_button.setEnabled(False)
        self.response.setText("")

        self.worker = NovaWorker()

        self.worker.finished.connect(
            self.nova_finished
        )

        self.worker.error.connect(
            self.nova_error
        )

        self.worker.start()

    def nova_finished(self, result):

        self.status.setText("Ready")

        self.talk_button.setText("🎙  TALK")

        self.talk_button.setEnabled(True)

        self.response.setText(result)

    def nova_error(self, error):

        self.status.setText("Something went wrong")

        self.talk_button.setText("🎙  TALK")

        self.talk_button.setEnabled(True)

        self.response.setText(
            f"Error:\n{error}"
        )


def main():

    app = QApplication(sys.argv)

    window = NovaApp()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()