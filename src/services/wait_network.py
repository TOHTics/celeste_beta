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
    output=subprocess.call(commandWvdial, stdout=fnull)

print ('Trying to open port')
port = None
start_time=time.time()
SECONDS_HOUR=10
flag4G=True
while 1:
    try:
        port = serial.Serial(port = "/dev/ttyUSB2",baudrate = 9600,rtscts = True,dsrdtr=True,bytesize=8,parity='N',stopbits=1)
        break
    except SerialException:
        print 'USB2 is not connected yet'
        sleep(.5)
        elapsed_time=time.time()-start_time
        if elapsed_time>=SECONDS_HOUR:
            flag4G=False
            print "timeout! there is not sim module connected"
            break
iniConfig={}
if flag4G==True:
    port.flush()
    time.sleep(5)
    print('Port opened, waiting for init')
    port.close()
    time.sleep(6)
    fout=open('wvidial.txt', 'w')
    fnull=open(os.devnull, 'w')
    comIfcDown=['sudo','ifconfig', 'wwan0', 'down']
    output=subprocess.call(comIfcDown, stdout=fnull)
    time.sleep(1)
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
            time.sleep(1000)#it's necessary for the subprocess wvdial thread
            print "sleeping..."



