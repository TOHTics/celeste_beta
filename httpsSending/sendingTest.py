import time
import os
import sys
import subprocess


def ping(interface, host, n=2):
    assert(n>2)
    fnull=open(os.devnull, 'w')
    fout=open('outputFile.txt', "w")
    stable=True
    for i in range(n):
        command = ['ping','-I', interface, '-c1', host]
        #command = ["ls", "-l"]
        output=subprocess.call(command, stdout=fnull)
        #sys.stdout=
        #print "output = ", output
        if output !=0:
            stable=False
            break
    return stable



if __name__=="__main__":
    if ping("eth1", "google.com", 5)==True:
        print "Succed!"
    else:
        print "didn't work"
