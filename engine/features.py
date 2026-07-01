import pygame
import eel
import os
from engine.config import ASSISTANT_NAME
from engine.command import *
import pywhatkit as pkt #playing assistant sound fn

import sqlite3
import webbrowser
import pvporcupine
import pyaudio
import struct

from engine.helper import extract_yt_term


connection = sqlite3.connect("Ultron.db")
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
    porcupine=None
    paud=None
    audio_stream=None #bg microphone

    try:


        # pre trained keywords
        porcupine=pvporcupine.create(keywords=["terminator"])
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16, input=True,frames_per_buffer=porcupine.frame_length)

        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic
            keyword_index=porcupine.process(keyword)

            # checking first keyword detected for not
            if keyword_index>=0:
                print("Hotword Detected")

                 # CLOSE HOTWORD MIC
                audio_stream.close()
                paud.terminate()

                # pressing shortcut key alt+u
                import pyautogui as autogui
                autogui.keyDown("alt")
                autogui.press("u")
                time.sleep(2)
                autogui.keyUp("alt")

                break

            
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
