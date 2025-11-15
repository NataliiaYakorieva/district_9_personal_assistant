import os
import time
from typing import Optional

from dotenv import load_dotenv
from groq import Groq
import speech_recognition as sr
import pyttsx3

#  ENV & CLIENT

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY not found in .env file. "
        "Please create .env and add GROQ_API_KEY=..."
    )

client = Groq(api_key=api_key)

#  SPEECH: TTS


recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Try to find a pleasant English female voice (for Mac it is often 'Samantha')
voices = engine.getProperty("voices")
for v in voices:
    name = getattr(v, "name", "").lower()
    if "samantha" in name or "female" in name or "english" in name:
        engine.setProperty("voice", v.id)
        break

engine.setProperty("rate", 180)  # speaking speed
engine.setProperty("volume", 1.0)  # max volume


def speak(text: str) -> None:
    """Speak the text aloud."""
    print(f"\nAssistant: {text}\n")
    engine.say(text)
    engine.runAndWait()


#  SPEECH: STT (ENGLISH ONLY)

def listen() -> Optional[str]:
    """
    Listen from microphone and return recognized English text.
    Returns None if nothing recognized or there was an error.
    """
    with sr.Microphone() as source:
        print("Listening... Speak into the microphone.")
        recognizer.adjust_for_ambient_noise(source, duration=1.0)

        try:
            audio = recognizer.listen(
                source,
                timeout=7,  # wait up to 7s for speech to start
                phrase_time_limit=10,  # max phrase length
            )
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None

    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(  # type: ignore[attr-defined]
            audio,
            language="en-US",
        )
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Speech not recognized.")
        return None
    except sr.RequestError as error:
        print(f"Speech recognition service error: {error}")
        return None


# -----------------------
#  GROQ CHAT
# -----------------------

def ask_groq(user_text: str) -> str:
    """Send text to Groq model and return its response."""
    system_prompt = (
        "You are a friendly and helpful AI voice assistant. "
        "Always answer in simple, short, clear English. "
        "Use 1–3 short sentences only."
    )

    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,  # type: ignore[arg-type]
            temperature=0.2,
        )

        message = response.choices[0].message.content or ""
        answer = message.strip()
        if not answer:
            return "Sorry, I do not know how to answer that."
        return answer

    except Exception as error:  # noqa: BLE001
        print(f"Groq error: {error!r}")
        return "I had a problem contacting the AI service. Please try again."


# -----------------------
#  MAIN LOOP
# -----------------------

def main() -> None:
    """Main loop of the voice assistant."""
    speak(
        "Hello! I am your Groq voice assistant. "
        "You can ask me anything in English."
    )

    while True:
        print("Say something (or say 'stop', 'exit', or 'bye' to quit)...")
        user_text = listen()

        if not user_text:
            continue

        lowered = user_text.lower().strip()
        if lowered in {"stop", "exit", "quit", "bye", "goodbye"}:
            speak("Okay, shutting down. Goodbye!")
            break

        answer = ask_groq(user_text)
        speak(answer)

        time.sleep(0.3)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted manually.")
