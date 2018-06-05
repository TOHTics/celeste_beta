import serial
import time
from serial import SerialException
from time import sleep
import os
import sys
import subprocess
import json
import thread


def launchWvdial(threadName):
    commandWvdial = ['sudo','wvdial', '&']
    fnull=open(os.devnull, 'w')
    print "ppp0 goes up"
    output=subprocess.call(commandWvdial, stdout=fnull)
    time.sleep(10)
    fnull=open(os.devnull, 'w')

print ('Trying to open port')
port = None
start_time=time.time()
SECONDS_HOUR=35
flag4G=True
#p = subprocess.Popen(["sudo", "ifconfig", "|", "grep", "eth0"], stdout=subprocess.PIPE)
#print p.communicate()
while 1:
    try:
        port = serial.Serial(port = "/dev/ttyUSB2",baudrate = 9600,rtscts = True,dsrdtr=True,bytesize=8,parity='N',stopbits=1)
        break
    except SerialException:
        print 'USB2 is not connected yet'
        sleep(.6)
        elapsed_time=time.time()-start_time
        if elapsed_time>=SECONDS_HOUR:
            flag4G=False
            print "timeout! there is not sim module connected"
            break
iniConfig={}
if flag4G==True:
    port.flush()
    print "sim module detected"
    time.sleep(3)
    print('Port opened, waiting for init')
    port.close()
    time.sleep(6)
    fout=open('wvidial.txt', 'w')
    fnull=open(os.devnull, 'w')
    comIfcDown=['sudo','ifconfig', 'wwan0', 'down']
    output=subprocess.call(comIfcDown, stdout=fnull)
    time.sleep(.5)
    try:
        thread.start_new_thread(launchWvdial, ("Thread wvdial", ) )
    except:
        print "Error: unable to start wvdial thread"

    #output=subprocess.call(commandWvdial, stdout=fnull)
    #process = subprocess.Popen(commandWvdia, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    #stdout, stderr = process.communicate()
    #print "after subprocess!!!!!!!\n\n"
    time.sleep(5)
    iniConfig={'intSim':"1"}

else:
    time.sleep(6)
    fnull=open(os.devnull, 'w')
    comIfcDown=['sudo','ifconfig', 'wwan0', 'down']
    output=subprocess.call(comIfcDown, stdout=fnull)
    iniConfig={'intSim':"0"}
    time.sleep(2)


start_time=time.time()

strPPP0=""
if flag4G==True:
    while True:#waits until the ppp0 is up
        ifconfigCmd=subprocess.Popen(["sudo", "ifconfig"], stdout=subprocess.PIPE)
        try:
            strPPP0=subprocess.check_output(('grep', 'ppp0'), stdin=ifconfigCmd.stdout)
        except:
            print "there is not ppp0"

        print "grep ppp0 output: ",strPPP0
        if "ppp0" in strPPP0:
            print "the ppp0 is up "
            print "ppp0 goes down"
            comIfcDown=['sudo','ifconfig', 'ppp0', 'down']#necessary to the principal firmware takes control over the network intefaces
            output=subprocess.call(comIfcDown, stdout=fnull)
            break

        elapsed_time=time.time()-start_time
        if elapsed_time>=8:#
            print "timeout! there is not ppp0 interface"#maybe the antenna is disconnected
            print "killing wvdial"
            comIfcDown=['sudo','killall', 'wvdial']#necessary to the principal firmware takes control over the network intefaces
            output=subprocess.call(comIfcDown, stdout=fnull)
            flag4G=False
            iniConfig={'intSim':"0"}
            break

with open('configJson.txt', 'w') as outfile:
    json.dump(iniConfig, outfile)
    outfile.close()
time.sleep(4)

with open('configJson.txt') as json_file:
    dataConfig=json.load(json_file)
    print "json file: ", dataConfig['intSim']
    json_file.close()

    if flag4G==True:
        while True:
            print "sleeping..."
            time.sleep(90000)#it's necessary for the wvdial subprocess  thread



