import time
import os
import sys
import subprocess
import zlib


#def (interface, host, n=2):
#    print




if __name__=="__main__":
    s="the quick brown fox jumps over the lazy dog m going through the python.org's python tutorial, at the moment. I'm on 10.9 and I am trying to use the zlib library to compress a string. However, the len(compressedString) isn't always less than the len(originalString). My interpreter code is below:"
    print "length = ", len(s)
    t=zlib.compress(s)
    print "compressed = ", len(t)
    print "decompressed = ", zlib.decompress(t)








