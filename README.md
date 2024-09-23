
# Voice-Enabled AI Assistant

This project is a **Voice-Enabled AI Assistant** powered by the **Gemini API** for natural language understanding, **Google Speech Recognition** for converting speech to text, and **Pyttsx3** for text-to-speech synthesis. The application features a GUI built using **PyQt5**, making it interactive and user-friendly. The assistant can record your voice, convert it into text, send it to the AI for processing, and provide spoken responses, offering a natural, conversational experience.

## Features

- **Voice Recognition**: Converts speech to text using Google Speech Recognition.
- **Natural Language Processing**: Interacts with the Gemini API to process user queries and provide AI responses.
- **Text-to-Speech**: Uses Pyttsx3 to speak out the AI's response.
- **GUI**: A graphical user interface built with PyQt5, offering a seamless user experience.
- **Error Handling**: Provides clear feedback for any errors during speech recognition or AI processing.
- **Non-blocking UI**: Audio recording and AI response processing occur in separate threads, ensuring the interface remains responsive.
- **Customizable Interface**: Includes a pulsating "Start Recording" button to visually indicate when the recording is active.

## Installation

### Prerequisites

1. **Python 3.x** installed on your machine. You can download it from [here](https://www.python.org/downloads/).
2. **Gemini API Key**: You need to sign up for an API key from [Google's Gemini API platform](https://developers.google.com/) and replace the placeholder key (`API_KEY = 'Your_Gemini_API_Key'`) in the code with your actual API key.
3. **PyQt5**: Used for creating the GUI interface.
4. **SpeechRecognition** and **Pyttsx3**: For voice-to-text and text-to-speech functionality.

### Libraries

To install the required Python libraries, run the following command in your terminal:

```bash
pip install PyQt5 SpeechRecognition pyttsx3 google-generativeai sounddevice scipy
```

### Clone the Repository

```bash
git clone https://github.com/yourusername/voice-enabled-ai-assistant.git
cd voice-enabled-ai-assistant
```

### Running the Application

Once all the libraries are installed, run the following command to launch the application:

```bash
python main.py
```

### Main Functionalities

#### 1. Recording Audio
The app starts recording audio when you press the "Start Recording" button. It uses the `AudioRecorder` class to record the audio for a specified duration (default: 5 seconds).

#### 2. Speech-to-Text Conversion
The recorded audio is converted to text using Google’s SpeechRecognition library. The function `speech_to_text()` handles the conversion.

#### 3. AI Processing
The recognized text is sent to the **Gemini AI model**, which processes the message and returns a response. The function `AIProcessor.run()` is responsible for sending and receiving AI responses.

#### 4. Text-to-Speech
Once the AI returns the response, the `text_to_speech()` function converts the AI's text response back to speech and speaks it out loud.

#### 5. UI Interaction
The GUI is built using PyQt5, with clear status messages and a pulsating button indicating when the app is recording or processing.

## Code Structure

- `main.py`: This is the main file where the entire application logic resides.
  - **`AudioRecorder`**: A thread-safe class responsible for recording audio using `sounddevice`.
  - **`AIProcessor`**: A thread-safe class for sending text to the Gemini AI and handling responses.
  - **`PulsatingButton`**: Custom PyQt5 button with a pulsating effect to indicate active recording.
  - **`MainWindow`**: Main window of the application with GUI components like the conversation area, buttons, and status label.

## Future Improvements

- **Voice Command Customization**: Allow users to define custom commands for specific tasks.
- **Multiple Language Support**: Expand the app to recognize and respond in multiple languages.
- **Voice Feedback Improvements**: Add tone adjustments to text-to-speech responses for a more natural conversation flow.

## Contributing

Feel free to contribute to this project by submitting a pull request or opening an issue on GitHub.

## License

This project is licensed under the MIT License.
