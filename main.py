import os
import threading
import eel

from engine.features import *
from engine.command import *

from engine.state import hotword_paused

def start():
    eel.init("www")

    playStartupSound()
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    threading.Thread(target=playRemainingSound, daemon=True).start()
    threading.Thread(target=hotword, daemon=True).start()   # <-- new

    eel.start("index.html", mode=None, host="localhost", block=True)

# def start():
#     # initialize eel
#     eel.init("www")

#     # PLAY FIRST SOUND FULLY
#     playStartupSound()

#     # OPEN APP
#     os.system(
#         'start msedge.exe --app="http://localhost:8000/index.html"'
#     )

#     # PLAY SECOND SOUND IN BACKGROUND
#     threading.Thread(
#         target=playRemainingSound,
#         daemon=True
#     ).start()

#     # START EEL
#     eel.start(
#         "index.html",
#         mode=None,
#         host="localhost",
#         block=True
#     )

    