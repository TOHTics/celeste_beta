#!/usr/bin python
#from Emonlib import EnergyMonitor as EnergyMonitor
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import imp


if __name__ == "__main__":
    
    Emon=imp.load_source('EnergyMonitor', '/home/pi/Documents/celeste_beta/lib/emonpi/Emonlib.py')
    SPI_PORT=0
    SPI_DEVICE=0
    myMcp=Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    emon1=Emon.EnergyMonitor(myMcp)

    emon1.setVoltage(0, 1500, 1.6)
    emon1.setCurrent(1, 90.9)
    emon1.calcVI(80, 2)

