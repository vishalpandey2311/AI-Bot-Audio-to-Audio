import sys
import os
import asyncio
import google.generativeai as ai
import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QFrame, QScrollArea, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QRunnable, QThreadPool
from PyQt5.QtGui import QFont, QColor, QPalette

# API Key for Gemini AI (replace with your actual key)
API_KEY = 'YOUR_API_KEY'

# Configure AI and initialize chat
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

class AudioRecorder(QRunnable):
    """Runnable for recording audio without blocking the GUI"""
    def __init__(self, duration=5, sample_rate=16000):
        super().__init__()
        self.duration = duration
        self.sample_rate = sample_rate
        self.audio = None

    def run(self):
        """Record audio"""
        self.audio = sd.rec(int(self.duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='int16')
        sd.wait()

class AIProcessor(QRunnable):
    """Runnable for processing AI requests without blocking the GUI"""
    def __init__(self, message, callback):
        super().__init__()
        self.message = message
        self.callback = callback

    def run(self):
        """Process AI request"""
        try:
            response = chat.send_message(self.message)
            self.callback(response.text)
        except Exception as e:
            self.callback(f"Error processing AI request: {e}")

class PulsatingButton(QPushButton):
    """Custom button that pulsates when active"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setup_style()
        self.setup_animation()

    def setup_style(self):
        """Set up the button's visual style"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)
        self.setFixedSize(200, 200)

    def setup_animation(self):
        """Set up the pulsating animation"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.pulsate)
        self.pulsating = False
        self.pulse_size = 200

    def pulsate(self):
        """Change button size to create pulsating effect"""
        if self.pulsating:
            self.pulse_size = 190 if self.pulse_size == 200 else 200
            self.setFixedSize(self.pulse_size, self.pulse_size)

    def start_pulsating(self):
        """Start the pulsating animation"""
        self.pulsating = True
        self.timer.start(500)

    def stop_pulsating(self):
        """Stop the pulsating animation"""
        self.pulsating = False
        self.timer.stop()
        self.setFixedSize(200, 200)

class ConversationWidget(QWidget):
    """Widget for displaying a single message in the conversation"""
    def __init__(self, text, is_user):
        super().__init__()
        self.setup_ui(text, is_user)

    def setup_ui(self, text, is_user):
        """Set up the UI for the message"""
        layout = QHBoxLayout()
        message = QLabel(text)
        message.setWordWrap(True)
        message.setStyleSheet(f"""
            background-color: {'#E8F5E9' if is_user else '#E1F5FE'};
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
        """)
        if is_user:
            layout.addStretch()
        layout.addWidget(message)
        if not is_user:
            layout.addStretch()
        self.setLayout(layout)

class MainWindow(QMainWindow):
    """Main window of the application"""
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_connections()
        self.threadpool = QThreadPool()
        self.is_recording = False

    def setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("Voice-enabled AI Assistant")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #F0F4F8;")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # Set up the conversation area
        self.setup_conversation_area(layout)

        # Set up the button layout
        button_layout = QHBoxLayout()
        self.setup_record_button(button_layout)
        self.setup_stop_button(button_layout)
        layout.addLayout(button_layout)

        # Set up the status label
        self.setup_status_label(layout)

        main_widget.setLayout(layout)

    def setup_conversation_area(self, layout):
        """Set up the scrollable conversation area"""
        self.conversation_area = QScrollArea()
        self.conversation_area.setWidgetResizable(True)
        self.conversation_area.setStyleSheet("""
            QScrollArea {
                border: 2px solid #B0BEC5;
                border-radius: 15px;
                background-color: white;
            }
        """)
        self.conversation_widget = QWidget()
        self.conversation_layout = QVBoxLayout(self.conversation_widget)
        self.conversation_area.setWidget(self.conversation_widget)
        layout.addWidget(self.conversation_area)

    def setup_record_button(self, layout):
        """Set up the record button"""
        self.record_button = PulsatingButton("Start Recording")
        layout.addWidget(self.record_button)

    def setup_stop_button(self, layout):
        """Set up the stop button"""
        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
            QPushButton:pressed {
                background-color: #B71C1C;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        layout.addWidget(self.stop_button)

    def setup_status_label(self, layout):
        """Set up the status label"""
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #1565C0;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.status_label)

    def setup_connections(self):
        """Set up button connections"""
        self.record_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

    def start_recording(self):
        """Start the audio recording process"""
        self.status_label.setText("Recording...")
        self.record_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.record_button.start_pulsating()
        self.is_recording = True
        self.recorder = AudioRecorder()
        self.threadpool.start(self.recorder)

    def stop_recording(self):
        """Stop the audio recording process"""
        if self.is_recording:
            self.is_recording = False
            self.status_label.setText("Processing...")
            self.stop_button.setEnabled(False)
            self.record_button.stop_pulsating()
            self.process_audio()

    def process_audio(self):
        """Process the recorded audio"""
        if hasattr(self.recorder, 'audio') and self.recorder.audio is not None:
            self.save_audio(self.recorder.audio.flatten())
            message = self.speech_to_text("temp.wav")
            self.add_message_to_conversation(message, True)

            if message.lower() == 'close':
                self.close()
                return

            self.status_label.setText("AI is thinking...")
            processor = AIProcessor(message, self.handle_ai_response)
            self.threadpool.start(processor)
        else:
            self.status_label.setText("Failed to record audio")
            self.record_button.setEnabled(True)

    def handle_ai_response(self, response_text):
        """Handle the AI response"""
        self.add_message_to_conversation(response_text, False)
        self.text_to_speech(response_text)
        self.status_label.setText("Ready")
        self.record_button.setEnabled(True)

    def add_message_to_conversation(self, text, is_user):
        """Add a message to the conversation"""
        message_widget = ConversationWidget(text, is_user)
        self.conversation_layout.addWidget(message_widget)
        self.conversation_area.verticalScrollBar().setValue(self.conversation_area.verticalScrollBar().maximum())

    def speech_to_text(self, file_path):
        """Convert speech to text"""
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results; {e}"

    def save_audio(self, audio_data, file_name="temp.wav"):
        """Save the recorded audio to a WAV file"""
        wavfile.write(file_name, 16000, audio_data.astype(np.int16))

    def text_to_speech(self, text):
        """Convert text to speech"""
        engine.say(text)
        engine.runAndWait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
