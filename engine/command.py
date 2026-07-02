import speech_recognition as sr
import eel
import time

from engine.speech import speak
from engine.features import openCommand, PlayYoutube
from engine.state import hotword_paused


def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("listening.....")
        eel.DisplayMessage("Listening.....")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)

        audio = r.listen(source, timeout=5, phrase_time_limit=8)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing.....")
        query = r.recognize_google(audio, language="en-in")
        print(f"User: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)

    except Exception as e:
        return "Couldn't Hear You....."

    return query.lower()


@eel.expose
def allCommand():
    hotword_paused.set()   # tell hotword thread to stop reading the mic

    try:
        query = takecommand()
        print(query)

        if "open" in query:
            openCommand(query)
        elif "on youtube" in query:
            PlayYoutube(query)
        else:
            print("Not run")

    except Exception as e:
        print("Error :/", e)

    finally:
        hotword_paused.clear()   # let hotword thread resume

    eel.ShowHood()


# import pyttsx3
# import speech_recognition as sr
# import eel
# import time

# from engine.features import *

# from engine.state import hotword_paused

# def speak(text):
#     engine = pyttsx3.init('sapi5')
#     voices = engine.getProperty('voices')      # getting details of current voice
#     engine.setProperty('voice', voices[0].id)
#     engine.setProperty('rate', 175)     # setting up new voice rate
#     eel.DisplayMessage(text)
#     # print(voices)
#     engine.say(text)
#     engine.runAndWait()



# def takecommand():

#     r = sr.Recognizer()

#     with sr.Microphone() as source:
#         print("listening.....")
#         # time.sleep(1)
#         eel.DisplayMessage("Listening.....")
#         r.pause_threshold = 1
#         r.adjust_for_ambient_noise(source, duration=1)

#         audio = r.listen(source, timeout=5, phrase_time_limit=8)

#     try:
#         print("Recognizing...")
#         eel.DisplayMessage("Recognizing.....")
#         query = r.recognize_google(audio, language="en-in")
#         print(f"User: {query}")
#         eel.DisplayMessage(query)
#         time.sleep(2)
#         # speak(query)

#     except Exception as e:
#         return "Couldn't Hear You....."

#     return query.lower()


# # text = takecommand()
# # speak(text)
 

# @eel.expose
# def allCommand():
#     hotword_paused.set()   # tell hotword thread to stop reading the mic

#     try:
#         query = takecommand()
#         print(query)

#         if "open" in query:
#             openCommand(query)
#         elif "on youtube" in query:
#             PlayYoutube(query)
#         else:
#             print("Not run")

#     except Exception as e:
#         print("Error :/", e)

#     finally:
#         hotword_paused.clear()   # let hotword thread resume

#     eel.ShowHood()