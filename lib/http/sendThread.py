#!/usr/bin/python

import threading
import time
import subprocess
import os
import sys
import imp

exitFlag = False

class myThread(threading.Thread):
    def __init__(self, threadID, name, myDb_, idDevice_):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.name=name
        self.myDb=myDb_
        self.wakeUp=15#every n secs check if is there available data in the table
        self.maxTries=3
        httpCom=imp.load_source('httpPackage', '/home/pi/Documents/celeste_beta/lib/http/httpPackage.py')
        self.myHttpCom=httpCom.Package2Send(idDevice_)

        #self.counter=counter
    
    def run(self):
        print "starting "+self.name+ " thread"
        while True:
            if self.myDb.getNElements()>0:#check the number of elements without send
                print "elements in table = ", self.myDb.getNElements()
                self.try2Send()
            else:
                print " empty table"
            print "go to sleep"
            time.sleep(self.wakeUp)
                #try to send all of them

    def try2Send(self):
        triesCount=0
        while self.myDb.getNElements()>0:
            if triesCount>=self.maxTries:
                print "sending fails, i'll try it later "
                break
            topElement=self.myDb.getTopElement()#xml from the table
            topElement=topElement[0][0]
            print " retrieved = ", topElement
            iterface=0
            #try first with eth0
            if ping("eth0", "google.com", 4)==True:
                print "eth0 connection succed!"
                interface=1
            else:#couldn' launch eth0, tries with ppp0
                if launchPPP0()==True:
                    print "succed launching ppp0"
                    if ping("ppp0", "google.com", 3)==True:
                        print "ppp0 nternet connection succed!"
                        interface=2
                    else:
                        interface=0
                    dropPPP0()
                else:
                    print "fail launching ppp0"
                    interface=0
            if interface>0:
                #sendData
                print"sending data..."
                serverResponse=self.myHttpCom.sendXml(topElement)
                print "server response = ", serverResponse
                if serverResponse==200:#data arrives well to server
                    print "the server received the data"
                    self.myDb.deleteTopElement()
                    triesCount=0
                else:
                    print "the data didn't arrive to server"
                    triesCount+=1

                """
                if the sending arrives well erases that element with:
                self.myDb.deleteTopElement()
                and set triesCount to 0
                if it does not arrive, it doesn't use the function and increment the counter:
                triesCount+=1
                """
            else:
                triesCount+=1

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
    if out!=0:
        return False
    command=['sudo', 'route', 'add', 'default', 'dev', 'ppp0']
    time.sleep(.5)
    out=subprocess.call(command, stdout=fout2)#set ppp0 as first option in the interfaces
    if out==1:
        return True
    else:
        return False

def dropPPP0():
    fout=open('dropsPPPOut.txt', 'w')
    command = ['sudo', 'ifconfig','ppp0', 'down']
    out=subprocess.call(command, stdout=fout)#rise the ppp0 interface


    """
    def print_time(self, delay):
        while self.counter:
            if exitFlag:
                self.name.exit()
            time.sleep(delay)
            print "%s: %s" % (self.name, time.ctime(time.time()))
            self.counter -= 1
            """



