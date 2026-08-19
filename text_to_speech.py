import pyttsx3


def speak(text):

    print("\nAI Speaking...")

    engine = pyttsx3.init()

    try:
        engine.setProperty("rate", 165)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()

    finally:
        engine.stop()
        del engine

    print("AI finished speaking.")