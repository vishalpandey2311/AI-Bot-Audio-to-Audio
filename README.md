# AI Bot Project

This AI bot is a console-based application built in Python. It interacts with users, sends user input to the **Gemini API**, and returns the AI's response back to the user. The bot is designed to engage in meaningful conversations and is hosted on **PythonAnywhere** for live use. The project uses a simple architecture with a focus on easy deployment and use.

---

## Features

- **Gemini API Integration**: The AI bot leverages the power of the Gemini API to generate responses based on user input.
- **Console-Based Interface**: Users can interact with the AI directly from the console.
- **Live Hosting**: The bot is hosted on PythonAnywhere, but can also be run locally.
- **Simple Workflow**: Easy to understand and extend for further customization.

---

## Functions and Workflow

### 1. `get_user_input()`
This function collects user input from the console.
```python
def get_user_input():
    user_input = input("You: ")
    return user_input
```
- **Purpose**: To gather input from the user.
- **Workflow**: The user enters a message, which is stored and returned to be sent to the Gemini API.

### 2. `send_to_gemini_api(user_input)`
This function sends the user's input to the Gemini API and retrieves a response.
```python
def send_to_gemini_api(user_input):
    # Use HTTP requests to communicate with Gemini API
    response = send_request_to_gemini(user_input)
    return response
```
- **Purpose**: To send the user's input to the AI and get the AI's response.
- **Workflow**: The function makes an HTTP request to the Gemini API, passing in the user's message and awaiting the response.

### 3. `process_response(response)`
This function processes the response received from the Gemini API.
```python
def process_response(response):
    return response['data']['message']
```
- **Purpose**: To extract the actual message from the API response.
- **Workflow**: It processes the JSON object returned by the API, extracting and returning the relevant message.

### 4. `display_bot_response(bot_response)`
This function outputs the AI's response in the console.
```python
def display_bot_response(bot_response):
    print(f"Bot: {bot_response}")
```
- **Purpose**: To display the response from the Gemini API in the console.
- **Workflow**: The processed message is displayed to the user in the console format.

### 5. `main()`
This is the main function that ties all the components together.
```python
def main():
    print("Welcome to the AI Console Bot!")
    while True:
        user_input = get_user_input()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = send_to_gemini_api(user_input)
        bot_response = process_response(response)
        display_bot_response(bot_response)
```
- **Purpose**: To control the overall flow of the application.
- **Workflow**:
  1. The bot welcomes the user.
  2. It runs in a continuous loop, asking for input, sending it to the Gemini API, processing the response, and displaying the result.
  3. The loop exits when the user types 'exit'.

---

## Getting Started

### Prerequisites
- Python 3.x installed on your system.
- Internet connection (for interacting with the Gemini API).
- A PythonAnywhere account (if you wish to host the bot).

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ai-bot.git
   cd ai-bot
   ```

2. **Install the required Python libraries**:
   ```bash
   pip install -r requirements.txt
   ```
   > Ensure you have the necessary dependencies such as `requests` to handle the API requests.

3. **Configure API**:
   - Replace the `API_KEY` in the code with your Gemini API key.
   - Update any necessary API endpoint URLs as per your Gemini account.

### Running Locally

1. **Run the application**:
   ```bash
   python bot.py
   ```
   > The console bot will start, and you can begin interacting with the AI.

2. **Exit**:
   - Type `exit` to end the conversation and stop the program.

### Hosting on PythonAnywhere

1. **Create an account**: Sign up at [PythonAnywhere](https://www.pythonanywhere.com/).
2. **Upload your project**:
   - You can either upload the repository directly or clone it using `git clone` in the PythonAnywhere bash console.
3. **Setup**:
   - Install the required dependencies in the virtual environment provided by PythonAnywhere.
4. **Run your AI**: Once everything is set up, the bot will run live on PythonAnywhere.

---

## Future Enhancements

- **GUI Support**: Add a graphical user interface for enhanced user interaction.
- **Improved AI**: Implement more advanced NLP features and alternative AI models.
- **Customization**: Enable customizable responses and workflow behavior.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Contributors

- **Vishal Pandey** - Initial work and development.
