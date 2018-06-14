#!/usr/bin python
#from Emonlib import EnergyMonitor as EnergyMonitor
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import imp
import RPi.GPIO as GPIO  
import time
import sys
import datetime
import tools
import json
GPIO.setmode(GPIO.BCM)  

projectPath='/home/pi/Documents/celeste_beta/'
if __name__ == "__main__":
    
    print "starting at "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    relayPin=18
    #idDevice=sys.argv[1]
    
    with open('configFile.txt') as configFile:
        jsonConfig=json.load(configFile)
        configFile.close()
    idDevice=jsonConfig['id_device']
    N_PHASES=jsonConfig['phases']
    SECONDS_HOUR=jsonConfig['time_kw']#should be 3600, number of seconds in an hour to compute the kw/h, 300 for 5m
    Emon=imp.load_source('EnergyMonitor', '/home/pi/Documents/celeste_beta/lib/emonpi/Emonlib.py')
    Emon2=imp.load_source('EnergyMonitor', '/home/pi/Documents/celeste_beta/lib/emonpi/Emonlib.py')
    Emon3=imp.load_source('EnergyMonitor', '/home/pi/Documents/celeste_beta/lib/emonpi/Emonlib.py')
    Emon4=imp.load_source('EnergyMonitor', '/home/pi/Documents/celeste_beta/lib/emonpi/Emonlib.py')
    httpCom=imp.load_source('httpPackage', '/home/pi/Documents/celeste_beta/lib/http/httpPackage.py')
    myHttpCom=httpCom.Package2Send(idDevice)
    celesteDb=imp.load_source('dataBase', '/home/pi/Documents/celeste_beta/lib/Database/celestePg.py')
    myDatabase=celesteDb.CelesteDB("celestedb", "pi", "power_xml")

    SPI_DEVICE=1
    SPI_PORT=0
    myMcp=Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

    """CLK=3
    MISO=15
    MOSI=14
    CS=2
    myMcp=Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso = MISO, mosi=MOSI)"""
    
    
#******************thread to dequeue from the database and send to server, the main thread is inserting elements to the db
    with open(projectPath+'src/services/configJson.txt') as json_file:
        dataConfig=json.load(json_file)
        print "json file: ", dataConfig['intSim']
        json_file.close()
    simFlag=False
    if dataConfig['intSim']=='1':
        simFlag=True
        #print"The sim module is connected"
    elif dataConfig['intSim']=='0': 
        #print"The sim module is not connected"
        simFlag=False


    thread=imp.load_source('threadsManager', projectPath+'lib/http/sendThread.py')
    #create new threads
    myThread=thread.myThread(1, "thread-1", myDatabase, idDevice, simFlag, jsonConfig)
    #start new thread
    myThread.start()

#***********

    #CFE
    emon1=Emon.EnergyMonitor(myMcp)#phase 1
    emon2=Emon2.EnergyMonitor(myMcp)#phase 2

    #Paneles
    emon3=Emon3.EnergyMonitor(myMcp)#phase 1
    emon4=Emon4.EnergyMonitor(myMcp)#phase 2

    """
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Se activa la pulldown interna    
    voltSensor= GPIO.input(21)
    print "voasasltSensor = ", voltSensor
    #GPIOasas(21, GPIO.BOTH, callback=my_callback)#Se declara la interrupcion
    """

    emon1.setVoltage(0, 256, 1.6)#250
    emon1.setCurrent(1, 185)


    """
    emon2.setVoltage(2, 256, 1.6)
    emon2.setCurrent(3, 96)
    emon3.setVoltage(4, 250, 1.6)
    emon3.setCurrent(5, 90)

    emon4.setVoltage(6, 250, 1.6)
    emon4.setCurrent(7, 90)"""

    nSamples=0
    countEmons=0
    powSum=[]
    emonVec=[]
    powSum.extend([None]*N_PHASES)
    emonVec.extend([None]*N_PHASES)
    emonVec[0]=emon1
    #emonVec[1]=emon2
    #emonVec[1]=emon2
    powSum[0]=0.0#assigns type to the vector
    sumRealPow=0.
    print "settling readings..."
    tools.settleReadings(emonVec)
    start_time=time.time()
    while True:
        countEmons=0
        for currentEmon in emonVec:
            print "emon %d"% (countEmons)
            if currentEmon.calcVI(400, 10, True)==False:#estable con 500 muestras
                print "There is not voltage sensor"
            time.sleep(.05)
            sumRealPow+=currentEmon.realPower
            countEmons+=1

        #print "real power sum = ", sumRealPow
        powSum[0]+=sumRealPow
        sumRealPow=0.
        nSamples+=1
        print "\n"
        elapsed_time=time.time()-start_time
        #print "elapsed Time: ", elapsed_time
        if elapsed_time>=SECONDS_HOUR:
            print "elapsed time = ", elapsed_time
            print "samples = ", nSamples
            powSum[0]=powSum[0]/nSamples
            print "i'm going to save: ", powSum[0], "watts"
            tools.saveKw(powSum, myDatabase, myHttpCom)
            powSum[0]=0
            nSamples=0
            start_time=time.time()

        print "\n"
        time.sleep(5)

