from shlex import quote
import subprocess
import logging

import pyautogui
import pygame
import eel
import os
from engine.config import ASSISTANT_NAME
import pywhatkit as pkt #playing assistant sound fn

import sqlite3
import webbrowser
import pvporcupine
import pyaudio
import struct
import time

from engine.helper import extract_yt_term, remove_words

from engine.state import hotword_paused
from engine.speech import speak

logging.basicConfig(
    filename="ultron_log.txt",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s"
)
logging.info("=== features.py loaded ===")

connection = sqlite3.connect("Ultron.db", check_same_thread=False)
cursor = connection.cursor()

# initialize pygame mixer
pygame.mixer.init()

# preload sounds
startup_sound = pygame.mixer.Sound(
    "www/assets/audio/soundtrack1_segment_0_to_4.mp3"
)

remaining_sound = pygame.mixer.Sound(
    "www/assets/audio/soundtrack1_segment_4_to_6.mp3"
)

assistant_sound = pygame.mixer.Sound(
    "www/assets/audio/soundtrack2.mp3"
)


# FIRST SOUND
def playStartupSound():
    startup_sound.play()

    # wait until sound finishes
    while pygame.mixer.get_busy():
        continue


# SECOND SOUND
def playRemainingSound():
    remaining_sound.play()


# MIC BUTTON SOUND
@eel.expose
def playAssisstantSound():
    assistant_sound.play()

def openCommand(query):

    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")

    app_name = query.strip().lower()

    if app_name != "":

        try:

            # SEARCH IN SYSTEM COMMANDS
            cursor.execute(
                "SELECT path FROM sys_command WHERE LOWER(name)=?",
                (app_name,)
            )

            results = cursor.fetchall()

            # IF FOUND IN SYSTEM COMMANDS
            if len(results) != 0:

                speak("Opening " + app_name)

                os.startfile(results[0][0])

                return

            # SEARCH IN WEB COMMANDS
            cursor.execute(
                "SELECT path FROM web_command WHERE LOWER(name)=?",
                (app_name,)
            )

            results = cursor.fetchall()

            # IF FOUND IN WEB COMMANDS
            if len(results) != 0:

                speak("Opening " + app_name)

                webbrowser.open(results[0][0])

                return

            # FALLBACK
            speak("Opening " + app_name)

            os.system('start ' + app_name)

        except Exception as e:

            print(e)

            speak("Something went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on Youtube")
    pkt.playonyt(search_term)


def hotword():
    porcupine = None
    paud = None
    audio_stream = None

    try:
        # index 0 = wake word, index 1 = home word
        porcupine = pvporcupine.create(
    keywords=["terminator", "blueberry"],
    sensitivities=[0.7, 0.5]   # bump blueberry up, leave terminator as-is
)
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        while True:
            if hotword_paused.is_set():
                time.sleep(0.1)
                continue

            try:
                pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyword_index = porcupine.process(pcm)

                if keyword_index != -1:
                    print("Detected index:", keyword_index)

                if keyword_index == 0:
                    print("Wake hotword detected")
                    eel.showSiriWave()()

                elif keyword_index == 1: #not working right now even after changing the audio sensitivities
                    print("Home hotword detected")
                    eel.ShowHood()()

            except Exception as e:
                print("Hotword loop error:", e)
                continue

    except Exception as e:
        print("Hotword setup error:", e)
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



            
# finding contact
def findContact(query):

    logging.info(f"findContact called with query: {query}")

    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    logging.info(f"findContact query after word removal: '{query}'")

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()

        logging.info(f"findContact DB results: {results}")

        mobile_number_str = str(results[0][0]).replace(" ", "").replace("-", "")
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        logging.info(f"findContact success: number={mobile_number_str}, name={query}")
        return mobile_number_str, query
    except Exception as e:
        logging.exception("findContact error")
        speak('not exist in contacts')
        return 0, 0


# whatsapp calling/msg

CALL_ICON_PATH = "www/assets/images/call_icon.png"
VIDEO_ICON_PATH = "www/assets/images/video_icon.png"


def clickIcon(icon_path, label, confidence=0.8, attempts=3, wait_between=1.5):
    """
    Search the screen for icon_path and click its center.
    Retries a few times since WhatsApp may still be rendering.
    Returns True if clicked, False if never found.
    """
    for attempt in range(1, attempts + 1):
        try:
            location = pyautogui.locateCenterOnScreen(icon_path, confidence=confidence)
        except Exception as e:
            logging.exception(f"clickIcon error while searching for {label} (attempt {attempt})")
            location = None

        if location is not None:
            logging.info(f"clickIcon: found {label} at {location} on attempt {attempt}")
            pyautogui.click(location)
            return True

        logging.info(f"clickIcon: {label} not found on attempt {attempt}, retrying...")
        time.sleep(wait_between)

    logging.warning(f"clickIcon: {label} not found after {attempts} attempts")
    return False


def whatsApp(mobile_no, message, flag, name):

    logging.info(f"whatsApp called: mobile_no={mobile_no}, message={message}, flag={flag}, name={name}")

    if flag == 'message':
        ultron_message = "message send successfully to "+name

    elif flag == 'call':
        message = ''
        ultron_message = "calling to "+name

    else:
        message = ''
        ultron_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    logging.info(f"whatsApp URL: {whatsapp_url}")

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    result1 = subprocess.run(full_command, shell=True)
    logging.info(f"First subprocess.run returncode: {result1.returncode}")

    time.sleep(5)

    result2 = subprocess.run(full_command, shell=True)
    logging.info(f"Second subprocess.run returncode: {result2.returncode}")

    if flag == 'message':
        # unchanged from the original working version, no extra delay
        pyautogui.hotkey('ctrl', 'f')
        for i in range(1, 14):
            pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')
        speak(ultron_message)

    elif flag == 'call':
        # extra render time before searching for the icon
        time.sleep(2)
        found = clickIcon(CALL_ICON_PATH, "call icon")
        if found:
            speak(ultron_message)
        else:
            speak("could not find the call button on screen")

    else:
        # extra render time before searching for the icon
        time.sleep(2)
        found = clickIcon(VIDEO_ICON_PATH, "video call icon")
        if found:
            speak(ultron_message)
        else:
            speak("could not find the video call button on screen")

    logging.info("whatsApp function completed")