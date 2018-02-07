#!/usr/bin python
#from Emonlib import EnergyMonitor as EnergyMonitor
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import imp
import RPi.GPIO as GPIO  
import time
GPIO.setmode(GPIO.BCM)  

voltSensor=True #Para indicar que esta conectado el sensor
def my_callback(channel):  
    print " edge detected on port : ", channel
    print "- even though, in the main thread,"  
    print "waiting..."
    global voltSensor
    voltSensor= GPIO.input(21)
    if voltSensor==True:
        print "Rising edge"
    else:
        print "Falling detection"

    #time.sleep(10)
    #print "we are still waiting for a falling edge - how cool?\n"  


if __name__ == "__main__":
    
    Emon=imp.load_source('EnergyMonitor', '/home/pi/Documents/celeste_beta/lib/emonpi/Emonlib.py')
    SPI_PORT=0
    SPI_DEVICE=0
    myMcp=Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    emon1=Emon.EnergyMonitor(myMcp)

    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Se activa la pulldown interna    
    voltSensor= GPIO.input(21)
    print "voltSensor = ", voltSensor
    GPIO.add_event_detect(21, GPIO.BOTH, callback=my_callback)#Se declara la interrupcion
    print "sale"
    #GPIO.add_event_detect(21, GPIO.RISING, callback=my_callback2)#Se declara la interrupcion

    emon1.setVoltage(0, 250, 1.6)
    emon1.setCurrent(1, 90.9)

    while True:
        #emon1.setVoltage(0, 250, 1.6)
        #print "inside while = ", voltSensor
        #emon1.calcVI(260, 5, voltSensor)
        emon1.calcVI(500, 10, voltSensor)
        time.sleep(.5)



