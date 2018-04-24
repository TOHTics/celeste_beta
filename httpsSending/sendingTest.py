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
        output=subprocess.call(command, stdout=fout)
        #sys.stdout=
        #print "output = ", output
        if output !=0:
            stable=False
            break
    return stable


def launchPPP0():
    fout=open('pppOut.txt', 'w')
    fout2=open('pppOut2.txt', 'w')
    command = ['sudo', 'ifconfig','ppp0', 'up']
    out=subprocess.call(command, stdout=fout)#rise the ppp0 interface
    command=['sudo', 'route', 'add', 'default', 'dev', 'ppp0']
    time.sleep(.5)
    out=subprocess.call(command, stdout=fout2)#set ppp0 as first option in the interfaces

    print "out = ", out

def dropsPPP0():
    fout=open('dropsPPPOut.txt', 'w')
    command = ['sudo', 'ifconfig','ppp0', 'down']
    out=subprocess.call(command, stdout=fout)#rise the ppp0 interface
    print "out = ", out


s

if __name__=="__main__":

    #launchPPP0()
    #dropsPPP0()
    
    iterface=0
    #try first with eth0
    if ping("eth0", "google.com", 4)==True:
        print "eth0 Succed!"
        interface=1
    else:#try with ppp0
        print "didn't work eth0"
        print "launching ppp0..."
        launchPPP0()
        if ping("ppp0", "google.com", 3)==True:
            print "ppp0 succed!"
            interface=2
        else:
            print "didn't work ppp0 either"
            interface=0 #interface 0 means there are not internet connections

        dropsPPP0()







