import speech_recognition as sr
import pyttsx3
import asyncio
from googletrans import Translator


# -------------------------------
# Text To Speech Function
# -------------------------------
def speak(text, language="en"):

    engine = pyttsx3.init()

    # Speech speed
    engine.setProperty('rate', 150)

    # Available voices
    voices = engine.getProperty('voices')

    # Select voice
    if language == "en":
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)

    # Speak text
    engine.say(text)
    engine.runAndWait()


# -------------------------------
# Speech To Text Function
# -------------------------------
def speech_to_text():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("🎤 Please speak now in English...")

        # Reduce background noise
        recognizer.adjust_for_ambient_noise(source)

        # Listen from microphone
        audio = recognizer.listen(source)

    try:

        print("🔍 Recognizing Speech...")

        # Convert speech to text
        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print(f"✅ You said: {text}")

        return text

    except sr.UnknownValueError:

        print("❌ Could not understand the audio.")

    except sr.RequestError as e:

        print(f"❌ API Error: {e}")

    return ""


# -------------------------------
# Translate Text Function
# -------------------------------
async def translate_text(text, target_language="es"):

    translator = Translator()

    # Translate text
    translation = await translator.translate(
        text,
        dest=target_language
    )

    print(f"🌍 Translated Text: {translation.text}")

    return translation.text


# -------------------------------
# Display Language Options
# -------------------------------
def display_language_options():

    print("\n🌐 Available Translation Languages:\n")

    print("1. Hindi (hi)")
    print("2. Tamil (ta)")
    print("3. Telugu (te)")
    print("4. Bengali (bn)")
    print("5. Marathi (mr)")
    print("6. Gujarati (gu)")
    print("7. Malayalam (ml)")
    print("8. Punjabi (pa)")
    print("9. French (fr)")
    print("10. German (de)")

    choice = input(
        "\nPlease select the target language number: "
    )

    language_dict = {
        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "bn",
        "5": "mr",
        "6": "gu",
        "7": "ml",
        "8": "pa",
        "9": "fr",
        "10": "de"
    }

    return language_dict.get(choice, "es")


# -------------------------------
# Main Function
# -------------------------------
def main():

    # Select target language
    target_language = display_language_options()

    # Convert speech to text
    original_text = speech_to_text()

    # Check if speech recognized
    if original_text:

        # Translate text
        translated_text = asyncio.run(
            translate_text(
                original_text,
                target_language=target_language
            )
        )

        # Speak translated text
        speak(translated_text, language=target_language)

        print("\n✅ Translation spoken out successfully!")


# -------------------------------
# Program Start
# -------------------------------
if __name__ == "__main__":
    main()