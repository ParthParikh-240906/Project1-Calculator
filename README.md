# Project1-Calculator
# Calculator

A simple calculator built with Python and Streamlit. Supports add, subtract, multiply, divide, power, and square root — including voice input for numbers via your microphone.

## Features
- Tap-button interface (like a real calculator)
- Voice input: speak a number and it types the digits for you
- Basic error handling (divide by zero, invalid input, etc.)

## Running locally

1. Clone this repo and open the folder:
   ```bash
   git clone <your-repo-url>
   cd Project1-Calculator
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   streamlit run calculator_app.py
   ```

The app will open automatically in your browser at `http://localhost:8501`.

## Tech stack
- [Streamlit](https://streamlit.io/) — UI and app logic
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) — converts voice input to text (via Google's free Web Speech API)