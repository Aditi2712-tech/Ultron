import os
import threading #for playing audios in different threads
import eel #connecting backend to frontend using this lib

from engine.features import *

eel.init("www") #telling eel the dir containing frontend

# play first half
playStartupSound()

os.system("start msedge.exe --app=\"http://localhost:8000/index.html\"")

# play second half in background
threading.Thread(target=playRemainingSound, daemon=True).start()

eel.start("index.html", mode=None, host='localhost', block=True)