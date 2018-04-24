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
GPIO.setmode(GPIO.BCM)  


if __name__ == "__main__":
    
    relayPin=18
    idDevice=sys.argv[1]
    N_PHASES=1
    SECONDS_HOUR=20#should be 3600, number of seconds in an hour to compute the kw/h
    Emon=imp.load_source('EnergyMonitor', '/home/pi/Documents/celeste_beta/lib/emonpi/Emonlib.py')
    Emon2=imp.load_source('EnergyMonitor', '/home/pi/Documents/celeste_beta/lib/emonpi/Emonlib.py')
    Emon3=imp.load_source('EnergyMonitor', '/home/pi/Documents/celeste_beta/lib/emonpi/Emonlib.py')
    Emon4=imp.load_source('EnergyMonitor', '/home/pi/Documents/celeste_beta/lib/emonpi/Emonlib.py')
    httpCom=imp.load_source('httpPackage', '/home/pi/Documents/celeste_alpha/celeste/alpha/httpPackage.py')
    #myHttpCom=httpCom.Package2Send(idDevice)

    SPI_PORT=0
    SPI_DEVICE=1
    myMcp=Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    
    """CLK=3
    MISO=15
    MOSI=14
    CS=2
    myMcp=Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso = MISO, mosi=MOSI)"""

    #CFE
    emon1=Emon.EnergyMonitor(myMcp)#phase 1
    emon2=Emon2.EnergyMonitor(myMcp)#phase 2

    #Paneles
    emon3=Emon3.EnergyMonitor(myMcp)#phase 1
    emon4=Emon4.EnergyMonitor(myMcp)#phase 2

    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Se activa la pulldown interna    
    voltSensor= GPIO.input(21)
    print "voltSensor = ", voltSensor
    #GPIO.add_event_detect(21, GPIO.BOTH, callback=my_callback)#Se declara la interrupcion

    emon1.setVoltage(0, 250, 1.6)#250
    emon1.setCurrent(1, 150)

    """emon2.setVoltage(2, 250, 1.6)
    emon2.setCurrent(3, 90)

    emon3.setVoltage(4, 250, 1.6)
    emon3.setCurrent(5, 90)

    emon4.setVoltage(6, 250, 1.6)
    emon4.setCurrent(7, 90)"""

    start_time=time.time()
    nSamples=0
    powSum=[]
    powSum.extend([None]*N_PHASES)
    print "powSum = ", powSum

    while True:
        if emon1.calcVI(200, 5, True)==False:#estable con 500 muestras
            print "No se puede calcular la potencia en 1, no hay sensor de voltaje en esta fase"
        nSamples+=1
        powSum[0]+=emon1.realPower
        print "\n"
        elapsed_time=time.time()-start_time
        if elapsed_time>=SECONDS_HOUR:
            print "elapsed time = ", elapsed_time
            nSamples=0


        print "\n"
        time.sleep(.2)
        tools.computeKw()



