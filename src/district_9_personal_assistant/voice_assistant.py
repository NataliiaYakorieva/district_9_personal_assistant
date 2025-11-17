import os
import time

from dotenv import load_dotenv
from openai import OpenAI
import speech_recognition as sr
import pyttsx3

# INITIALIZATION


# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY not found in .env. Please check your .env file.")

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Initialize speech recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configure voice
voices = engine.getProperty("voices")

# Try to choose a more pleasant female English voice (Mac often has 'Samantha')
selected = False
for v in voices:
    name = getattr(v, "name", "").lower()
    if "samantha" in name or "female" in name:
        engine.setProperty("voice", v.id)
        selected = True
        break

# If nothing found, just keep default voice
# Make the speech a bit slower and clearer
engine.setProperty("rate", 180)  # default is usually around 200
engine.setProperty("volume", 1.0)  # max volume


def speak(text: str) -> None:
    """Speak the text aloud using the TTS engine."""
    print(f"\nAssistant: {text}\n")
    engine.say(text)
    engine.runAndWait()


def listen() -> str | None:
    """
    Listen to microphone input and return recognized text.
    Returns None if nothing recognized or an error occurs.
    """
    with sr.Microphone() as source:
        print("Listening... Speak into the microphone.")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,  # wait max 5 seconds for user to start speaking
                phrase_time_limit=15  # maximum length of spoken phrase
            )
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None

    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(
            audio,
            language="en-US"  # type: ignore[attr-defined]
        )
        print(f"You said: {text}")
        return text

    except sr.UnknownValueError:
        print("Speech not recognized.")
        return None

    except sr.RequestError:
        print("Speech recognition error.")
        return None


def ask_gpt(user_text: str) -> str:
    """Send text to GPT model and return its response."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly and helpful voice assistant. "
                        "Always reply in simple, short, clear English."
                    ),
                },
                {
                    "role": "user",
                    "content": user_text,
                },
            ],
        )
        answer = response.choices[0].message.content
        return answer.strip()
    except Exception as e:
        print("Error contacting OpenAI:", repr(e))
    return (
        "I had an error while communicating with ChatGPT."
    )


def main():
    """Main loop of the voice assistant."""
    speak(
        "Hello! I am your GPT voice assistant. "
        "You can ask me anything in English.")

    while True:
        print(
            "Say something (or say 'stop', 'exit', or 'bye' "
            "to quit)..."
        )
        user_text = listen()

        if not user_text:
            continue

        lower = user_text.lower().strip()
        if lower in ("stop", "exit", "quit", "bye", "goodbye"):
            speak("Okay, shutting down. Goodbye!")
            break

        answer = ask_gpt(user_text)
        speak(answer)

        time.sleep(0.3)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted manually.")
