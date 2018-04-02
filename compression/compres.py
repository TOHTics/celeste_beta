import time
import os
import sys
import subprocess
import zlib
import psycopg2


#def (interface, host, n=2):
#    print
fileName='./temp.txt'



if __name__=="__main__":
    s="the quick brown fox jumps over the lazy dog m going through the python.org's python tutorial, at the moment. I'm on 10.9 and I am trying to use the zlib library to compress a string. However, the len(compressedString) isn't always less than the len(originalString). My interpreter code is below:"+'\n'+" testing lineSkip..."
    #print "length = ", len(s)
    #t=zlib.compress(s)
    """print "compressed = ", t
    print "compressed = ", len(t)
    print "decompressed = ", zlib.decompress(t)"""

    #Functions to write the data
    if  os.path.isfile(fileName)==True:
        print "The file exists!" #If the file has content tries to send it
    else:
        print "the file does not exist, i'm going to create it"
        open(fileName, 'w').close()

    F=open(fileName, "r+")
    F.write(s)
    F.close()
    #print "s = ", s
    time.sleep(.5)
    F=open(fileName, "r+")
    content = F.readline()
    print "content = ", content
    print "content = ", F.readline()
    print "content = ", F.readline()
    F.close()



    








