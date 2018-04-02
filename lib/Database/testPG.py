import time
import os
import sys
import subprocess
import zlib
import psycopg2
import imp


#def (interface, host, n=2):
#    print
fileName='./temp.txt'

    


if __name__=="__main__":
    celesteDb=imp.load_source('dataBase', '/home/pi/Documents/celeste_beta/lib/Database/celestePg.py')
    myDatabase=celesteDb.CelesteDB("celestedb", "pi", "power_xml")
    newVal='<testing from python script 8>'
    results=myDatabase.getTopElement()
    print results
    myDatabase.deleteTopElement();
    print "top element deleted"
    results=myDatabase.getTopElement()
    print results



