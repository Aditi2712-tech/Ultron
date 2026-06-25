import pygame
import eel
import os
from engine.config import ASSISTANT_NAME
from engine.command import *
import pywhatkit as pkt
import re


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
    query.lower()

    if query!="":
        speak("Opening "+query)
        os.system('start '+query)
    else:
        speak("not found")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on Youtube")
    pkt.playonyt(search_term)

def extract_yt_term(command):
    #reg exp pattern to capture search term
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    #use re.search to find match in command
    match = re.search(pattern, command, re.IGNORECASE)
    #if match found, return extracted search term, or return home
    return match.group(1) if match else None