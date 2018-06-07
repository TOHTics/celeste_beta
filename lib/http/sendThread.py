#!/usr/bin/python

import threading
import time
import subprocess
import os
import sys
import imp

exitFlag = False

class myThread(threading.Thread):
    def __init__(self, threadID, name, myDb_, idDevice_, simFlag_, jsonConfig):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.name=name
        self.myDb=myDb_
        self.wakeUp=jsonConfig['wake_up']#every n secs check if is there available data in the table
        self.maxTries=jsonConfig['max_tries']
        self.simFlag=simFlag_
        httpCom=imp.load_source('httpPackage', '/home/pi/Documents/celeste_beta/lib/http/httpPackage.py')
        #print "starting thread with idDevice: ", idDevice_
        self.myHttpCom=httpCom.Package2Send(idDevice_)

        #self.counter=counter
    
    def run(self):
        print "starting "+self.name+ " thread"
        #time.sleep(self.wakeUp)#uncomment for not send inmediately
        while True:
            if self.myDb.getNElements()>0:#check the number of elements without send
                print "elements in table = ", self.myDb.getNElements()
                self.try2Send()
            else:
                print " empty table"
            print "go to sleep: %d"%(self.wakeUp)
            time.sleep(self.wakeUp)
                #try to send all of them

    def try2Send(self):
        triesCount=0
        while self.myDb.getNElements()>0:
            if triesCount>=self.maxTries:
                print "the submission failed several times, i'll try it later "
                break
            topElement=self.myDb.getTopElement()#xml from the table
            topElement=topElement[0][0]
            print " retrieved = ", topElement
            iterface=0
            #try first with eth0
            if ping("eth0", "google.com", 3)==True:
                print "eth0 connection succed!"
                interface=1
            elif self.simFlag==True:#couldn' use eth0, tries with ppp0
                print "The sim module is available"
                if launchPPP0()==True:#could be a bug here
                    print "succed launching ppp0"
                    if ping("ppp0", "google.com", 3)==True:
                        print "ppp0 internet connection succed!"
                        interface=2
                    else:
                        interface=0
                    dropPPP0()
                else:
                    dropPPP0()#eitherway
                    print "fail launching ppp0"
                    interface=0
                #resetEth0()#the driver could fail
            else:
                print "\n"
                print "The sim module and eth0 are not available "
                interface=0
                #resetEth0()#the driver could fail
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
            print "triesCount: %d"%(triesCount)
            time.sleep(.01)

def ping(interface, host, n=2):
    assert(n>2)
    print "trying ping with: ", interface
    fnull=open(os.devnull, 'w')
    fout=open('outputFile.txt', "w")
    stable=True
    for i in range(n):
        command = ['ping','-I', interface, '-c1', host, '-W8']
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
    print "ppp0 up output: ", out
    if out!=0:
        return False
    command=['sudo', 'route', 'add', 'default', 'dev', 'ppp0']
    time.sleep(.4)
    out=subprocess.call(command, stdout=fout2)#set ppp0 as first option in the interfaces
    print "route add output: ", out
    if out==0:
        return True
    else:
        return False

def dropPPP0():
    fout=open('dropsPPPOut.txt', 'w')
    command = ['sudo', 'ifconfig','ppp0', 'down']
    out=subprocess.call(command, stdout=fout)#rise the ppp0 interface

def resetEth0():#The ethernet driver (encj.. chip) has some problems
    fout=open(os.devnull, 'w')
    commandDown = ['sudo', 'ifconfig','eth0', 'down']
    out=subprocess.call(commandDown, stdout=fout)#rise the ppp0 interface
    time.sleep(.5)
    commandUp = ['sudo', 'ifconfig','eth0', 'up']
    out=subprocess.call(commandUp, stdout=fout)#rise the ppp0 interface


    """
    def print_time(self, delay):
        while self.counter:
            if exitFlag:
                self.name.exit()
            time.sleep(delay)
            print "%s: %s" % (self.name, time.ctime(time.time()))
            self.counter -= 1
            """



