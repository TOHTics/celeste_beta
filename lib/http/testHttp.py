import time
import os
import sys
import subprocess
import zlib
import psycopg2
import imp
import thread



if __name__=="__main__":
    print "iniciando..."
    celesteDb=imp.load_source('dataBase', '/home/pi/Documents/celeste_beta/lib/Database/celestePg.py')
    myDatabase=celesteDb.CelesteDB("celestedb", "pi", "power_xml")

    thread=imp.load_source('threadsManager', '/home/pi/Documents/celeste_beta/lib/http/sendThread.py')
    #create new threads
    myThread=thread.myThread(1, "thread-1", myDatabase, "a0001")

    #start new threads
    myThread.start()
    while True:
        pass


