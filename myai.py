# Import necessary libraries
import google.generativeai as ai  # For AI model interaction
import speech_recognition as sr  # For speech recognition
import pyttsx3  # For text-to-speech conversion
import sounddevice as sd  # For audio recording
import numpy as np  # For numerical operations
from scipy.io import wavfile  # For writing WAV files
import os  # For file operations
import re  # For regular expressions

# API Key for Gemini AI
API_KEY = 'YOUR_GEMINI-API-KEY'  # Replace with your actual Gemini API key

# Configure the AI API
ai.configure(api_key=API_KEY)

# Create a new generative AI model and start a chat
model = ai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def record_audio(duration=5, sample_rate=16000):
    """
    Record audio from the microphone.
    
    :param duration: Length of the recording in seconds
    :param sample_rate: Sample rate of the audio
    :return: Recorded audio as a numpy array
    """
    print("Listening...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    return audio.flatten()

def save_audio(audio, filename="temp.wav", sample_rate=16000):
    """
    Save the recorded audio to a WAV file.
    
    :param audio: Audio data as a numpy array
    :param filename: Name of the file to save
    :param sample_rate: Sample rate of the audio
    """
    wavfile.write(filename, sample_rate, audio)
    print(f"Audio saved to {filename}")
    print(f"File size: {os.path.getsize(filename)} bytes")

def speech_to_text(audio_file):
    """
    Convert speech from an audio file to text.
    
    :param audio_file: Path to the audio file
    :return: Recognized text or error message
    """
    print(f"Attempting to recognize speech from {audio_file}")
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Error: Could not understand audio")
        return "Speech recognition could not understand the audio"
    except sr.RequestError as e:
        print(f"Error: Could not request results from speech recognition service; {e}")
        return f"Could not request results from speech recognition service; {e}"

def clean_text(text):
    """
    Remove special characters from text, keeping common punctuation.
    
    :param text: Input text
    :return: Cleaned text
    """
    cleaned_text = re.sub(r'[^\w\s.,?!\'"]', '', text)
    return cleaned_text

def text_to_speech(text):
    """
    Convert text to speech and play it.
    
    :param text: Text to be converted to speech
    """
    cleaned_text = clean_text(text)  # Clean the text before passing to TTS
    engine.say(cleaned_text)
    engine.runAndWait()

# Main program loop
print("Voice-enabled AI Assistant")
print("Speak your message or say 'close' to exit")

while True:
    # Record audio
    audio = record_audio()
    save_audio(audio)
    
    # Convert speech to text
    message = speech_to_text("temp.wav")
    print("You said:", message)
    
    # Check if the user wants to exit
    if message.lower() == 'close':
        text_to_speech("Goodbye!")
        break
    
    # Send message to AI and get response
    response = chat.send_message(message)
    response_text = response.text
    print('AI:', response_text)
    
    # Convert AI response to speech
    text_to_speech(response_text)

print("Chat ended.")
