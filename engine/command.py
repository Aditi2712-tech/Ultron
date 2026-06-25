import pyttsx3
import speech_recognition as sr
import eel
import time


def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')      # getting details of current voice
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)     # setting up new voice rate
    eel.DisplayMessage(text)
    # print(voices)
    engine.say(text)
    engine.runAndWait()



def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("listening.....")
        # time.sleep(1)
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
        time.sleep(2)
        # speak(query)

    except Exception as e:
        return "Couldn't Hear You....."

    return query.lower()


# text = takecommand()
# speak(text)
 

@eel.expose
def allCommand():

    query = takecommand()
    print(query)

    if "open" in query:
        from engine.features import openCommand
        openCommand(query)
    elif "on youtube":
        from engine.features import PlayYoutube
        PlayYoutube(query)
    else:
        print("Not run")

    eel.ShowHood()
