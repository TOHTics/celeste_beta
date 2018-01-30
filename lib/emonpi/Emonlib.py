#!/usr/bin python

import time
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

class EnergyMonitor:

    def __init__(self):
      print("iniciando...")
      self.ADC_COUNTS=1024
      self.offsetV=self.ADC_COUNTS>>1#512
      self.offsetI=self.ADC_COUNTS>>1
      self.SPI_PORT=0
      self.SPI_DEVICE=0
      self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE))

      self.lastFilteredV=0
      self.filteredV=0          #Filtered_ is the raw analog value minus the DC offset
      self.filteredI=0
      self.sampleV=0 #raw analog value
      self.sampleI=0
      self.sqV=0
      self.sumV=0
      self.sqI=0
      self.sumI=0
      self.instP=0
      self.sumP=0
      self.phaseShiftedV=0
      self.lastVCross=False
      self.checkVCross=False

    def setVoltage(self, nChannel, calib, phase_shift):
        self.channelV=nChannel
        self.calibration=calib
        self.phase=phase_shift

    def setCurrent(self, nChannel, calib):
        self.channelI=nChannel
        self.calibration=calib
        self.startV=0

    #el numero de muestras esta definido por el numero de cruces (numero de medias ondas)
    def calcVI(self, crossings, timeout):
        SupplyVoltage=3300#puede leer del adc
        crossCount=0
        numberOfSamples=0

  #//-------------------------------------------------------------------------------------------------------------------------
  #// 1) Waits for the waveform to be close to 'zero' (mid-scale adc) part in sin curve.
  #//-------------------------------------------------------------------------------------------------------------------------
        st=False; #an indicator to exit the while loop
        start=time.clock()#Para que no se quede atorado en el loop
        while st==False:
            self.startV=self.mcp.read_adc(self.channelV)
            if self.startV<(self.ADC_COUNTS*0.55) and self.startV>(self.ADC_COUNTS*0.45):#Checa si esta en el rango (cercano al cero)
                st=True
            elapsedTime=time.clock()-start
            print elapsedTime
            if elapsedTime>timeout:
                st=True

        start=time.clock()
        crossCount=0
        nSamples=0
        while crossCount<crossings and (time.clock()-start)<timeout:
            nSamples+=1
            self.lastFilteredV=self.filteredV
            self.sampleV=self.mcp.read_adc(self.channelV)
            self.sampleI=self.mcp.read_adc(self.channelI)
        
            #Se aplica un flitro digital pasabajas para extraer, y se quita el offset de 1.65
            self.offsetV=self.offsetV+((self.sampleV-self.offsetV)/1024)
            self.filteredV=self.sampleV-self.offsetV
            self.offsetI=self.offsetI+((self.sampleI-self.offsetI)/1024)
            self.filteredI=self.sampleI-self.offsetI

            #Voltaje root-mean-square
            self.sqV=self.filteredV*self.filteredV
            self.sumV+=self.sqV

            #Corriente root-mean-square
            self.sqI=self.filteredI*self.filteredI
            self.sumI+=self.sqI

            #calibracion de fase
            self.phaseShiftedV=self.lastFilteredV+self.phase*(self.filteredV-self.lastFilteredV)

            #potencia instantanea
            self.instP=self.phaseShifted*self.filteredI
            self.sumP+=self.instP

            #Encontrar el No. de veces que el voltaje ha cruzado el voltaje inicial
            #Cada 2 cruces tendremos una muestra de la longitud de onda
            self.lastVCross=self.checkVCross
            if self.sampleV>self.startV:
                self.checkVCross=True
            else:
                 








#class MCP:#adc
#    def __init__(self):
#        self.SPI_PORT=0
#        self.SPI_DEVICE=0
#        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


