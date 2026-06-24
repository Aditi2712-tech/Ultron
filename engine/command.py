import pyttsx3
import speech_recognition as sr


def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')      # getting details of current voice
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)     # setting up new voice rate
    # print(voices)
    engine.say(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening.....")
        r.pause_threshold
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)

    try:
        print("Recognizing...")

        query = r.recognize_google(audio, language="en-in")
        print(f"User: {query}")
    except Exception as e:
        return ""

    return query.lower()


text = takecommand()
speak(text)


