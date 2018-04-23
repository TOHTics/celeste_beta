import time
import os
import sys
import subprocess
import zlib
import psycopg2
import imp
import thread


#def (interface, host, n=2):
#    print
fileName='./temp.txt'

    


if __name__=="__main__":
    print "iniciando..."
    while True:
        celesteDb=imp.load_source('dataBase', '/home/pi/Documents/celeste_beta/lib/Database/celestePg.py')
        myDatabase=celesteDb.CelesteDB("celestedb", "pi", "power_xml")
        newVal='<testing from python script 5>'
        #myDatabase.insertXml(newVal)
        results=myDatabase.getTopElement()
        print "top element = "
        print results
        #myDatabase.deleteTopElement();
        #print "top element deleted"
        
        """results=myDatabase.getTopElement()
        print "top element = "
        print results"""
        print "number of elements = ", myDatabase.getNElements()
        time.sleep(1)
        # Create two threads as follows
        try:
            thread.start_new_thread(myDatabase.threadTest, ("Thread-1", 2, ) )
            thread.start_new_thread( myDatabase.threadTest, ("Thread-2", 4, ) )
        except:
            print "Error: unable to start thread"

        while 1:
            pass


