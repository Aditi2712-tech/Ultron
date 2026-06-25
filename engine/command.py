import pyttsx3
import speech_recognition as sr
import eel


def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')      # getting details of current voice
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)     # setting up new voice rate
    # print(voices)
    engine.say(text)
    engine.runAndWait()


@eel.expose
def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("listening.....")
        eel.DisplayMessage("Listening.....")
        r.pause_threshold
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing.....")


        query = r.recognize_google(audio, language="en-in")
        print(f"User: {query}")
        eel.DisplayMessage(query)
        speak(query)
        eel.ShowHood()
    except Exception as e:
        return "Couldn't Hear You....."

    return query.lower()


# text = takecommand()
# speak(text)


