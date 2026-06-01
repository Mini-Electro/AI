import speech_recognition as sr
import pyttsx3
from googletrans import Translator

def speak(text, language="en"):
    engine = pyttsx3.init()

    engine.setProperty('rate',150)

    voices = engine.getProperty('voices')

    if language == "en":
        engine.setProperty('voice', voices[0].id)
    else:

        engine.setProperty('voice', voices[1].id)

    engine.say(text)

    engine.runAndWait()
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("???? Please speak now in english...")

        audio = recognizer.listen(source)
    try:
        print("???? Recognizing speech...")

        text = recognizer.recognize_google(audio, language="en-US")

        print(f"✅ You said: {text}")

        return text
    except sr.UnknownValueError:
        print("Couldn't understand the audio.")
    except sr.RequestError as e:
        print(f"API Error: {e}")

    return ""

def translate_text(text, target_language="es"):

    translator = Translator()

    translation = translator.translate(text, dest=target_language)

    print(f"???? Translated Text: {translation.text}")

    return translation.text

def display_language_options():
    print("???? Available translation languages:")

    print("1. English (en)")
    print("2. Spanish (es)")
    print("3. French (fr)")
    print("4. German (de)")
    print("5. Portuguese (pt)")
    print("6. Italian (it)")
    print("7. Chinese Simplified (zh-cn)")
    print("8. Japanese (ja)")
    print("9. Korean (ko)")
    print("10. Arabic (ar)")
    print("11. Hindi (hi)")
    print("12. Russian (ru)")

    choice = input("Please select the language target number (1-12): ")

    language_dict = {
        "1": "en",
        "2": "es",
        "3": "fr",
        "4": "de",
        "5": "pt",
        "6": "it",
        "7": "zh-cn",
        "8": "ja",
        "9": "ko",
        "10": "ar",
        "11": "hi",
        "12": "ru"
    }

    return language_dict.get(choice, "es")


def main():
    target_language = display_language_options()

    original_text = speech_to_text()

    if original_text:
        translated_text = translate_text(original_text, target_language=target_language)
        speak(translated_text, target_language)
        print("Translation spoken aloud!")

if __name__ == "__main__":
    main()