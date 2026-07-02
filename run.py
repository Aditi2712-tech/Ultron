from main import start

if __name__ == "__main__":
    start()





# import multiprocessing

# def runUltron(): #to run ultron
#     print("Process 1 is running")
#     from main import start
#     start()


# def listenHotWord(): #to run hotword
#     print("Process 2 is running")
#     from engine.features import hotword
#     hotword()

# # start both process
# if __name__ == "__main__":
#     p1 = multiprocessing.Process(target=runUltron)
#     p2 = multiprocessing.Process(target=listenHotWord)
#     p1.start()
#     p2.start()
#     p1.join()

#     if p2.is_alive():
#         p2.terminate()
#         p2.join()

#     print("System Stop")
