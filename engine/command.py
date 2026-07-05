import speech_recognition as sr
import eel
import time
import logging

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
        logging.info(f"allCommand query: {query}")

        if "open" in query:
            openCommand(query)
        elif "on youtube" in query:
            PlayYoutube(query)

        elif "send message" in query or "phone call" in query or "video call" in query or ("call" in query and "video" not in query):
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            logging.info(f"allCommand: contact_no={contact_no}, name={name}")

            if(contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()

                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'

                whatsApp(contact_no, query, flag, name)
            else:
                logging.info("allCommand: contact_no was 0, skipping whatsApp call")
        else:
            print("Not run")
            logging.info("allCommand: query matched no known command")

    except Exception as e:
        logging.exception("allCommand error")
        print("Error :/", e)

    finally:
        hotword_paused.clear()   # let hotword thread resume

    eel.ShowHood()