#!/usr/bin python

import time
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import math

class EnergyMonitor:

    def __init__(self, mcp_):
      #print("iniciando...")
      self.ADC_COUNTS=1024
      self.offsetV=self.ADC_COUNTS>>1#512
      self.offsetI=self.ADC_COUNTS>>1
      self.SPI_PORT=0
      self.SPI_DEVICE=0
      self.mcp = mcp_

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

      self.realPower=0
      self.apparentPower=0
      self.powerFactor=0
      self.Vrms=0
      self.Irms=0


    def setVoltage(self, nChannel, calibV, phase_shift):
        self.channelV=nChannel
        self.calibrationV=calibV
        self.phase=phase_shift

    def setCurrent(self, nChannel, calibI):
        self.channelI=nChannel
        self.calibrationI=calibI
        self.startV=0

    #el numero de muestras esta definido por el numero de cruces (numero de medias ondas)
    def calcVI(self, crossings, timeout, voltSensor):
        #print "channel", self.channelV
        SupplyVoltage=3300#puede leer del adc
        crossCount=0
        numberOfSamples=0
        #print "voltSensor = ", voltSensor

  #//-------------------------------------------------------------------------------------------------------------------------
  #// 1) Waits for the waveform to be close to 'zero' (mid-scale adc) part in sin curve.
  #//-------------------------------------------------------------------------------------------------------------------------
        st=False; #an indicator to exit the while loop
        start=time.time()#Para que no se quede atorado en el loop
        #print "Detectando que la signal este cercana a cero"
        countZero=0 #Contador de veces que esta dentro del rango cero
        self.startV=self.mcp.read_adc(self.channelV)
        #print "initial voltage = ", self.startV
        while st==False and voltSensor==True:
            self.startV=self.mcp.read_adc(self.channelV)
            #print "startV 1= ", self.startV
            if self.startV<(self.ADC_COUNTS*0.55) and self.startV>(self.ADC_COUNTS*0.45):#Checa si esta en el rango (cercano al cero)
            #if self.startV<(self.ADC_COUNTS*0.35) and self.startV>(self.ADC_COUNTS*0.25):#Checa si esta en el rango (cercano al cero)
             #   print "self.startV inside = ", self.startV
                countZero+=1
                #print "Detectado"
            if countZero==2:
             #   print "detectada"
                st=True
            elapsedTime=time.time()-start
            if elapsedTime>timeout:
                print "elapsedTime timeout"
                return False
                voltSensor=False
                #self.startV=0
                st=True
            #time.sleep(.001)

        start=time.time()
        crossCount=0
        nSamples=0
        timeout2=timeout
        #print " adc first reading: ", self.startV
        while crossCount<crossings and voltSensor==True: #Hasta ahora los calculos son erroneos puede ser por la frecuencia de muestreo
            if(time.time()-start)>=timeout2 and voltSensor==True:
                #self.sumV=0
                print "timeout!"
                break
            nSamples+=1
            self.lastFilteredV=self.filteredV
            self.sampleV=self.mcp.read_adc(self.channelV)
            self.sampleI=self.mcp.read_adc(self.channelI)
        
            #Se aplica un flitro digital pasabajas para extraer, y se quita el offset de 1.65
            self.offsetV=self.offsetV+((self.sampleV-self.offsetV)/1024.0)

            #print "offsetV dentro del while", self.offsetV
            self.filteredV=self.sampleV-self.offsetV
            self.offsetI=self.offsetI+((self.sampleI-self.offsetI)/1024.0)
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
            self.instP=self.phaseShiftedV*self.filteredI
            self.sumP+=self.instP

            #Encontrar el No. de veces que el voltaje ha cruzado el voltaje inicial
            #Cada 2 cruces tendremos una muestra de la longitud de onda
            self.lastVCross=self.checkVCross
            if self.sampleV>self.startV:
                self.checkVCross=True
            else:
                self.checkVCross=False
            if nSamples==1:
                self.lastVCross=self.checkVCross
            if self.lastVCross!=self.checkVCross:
                crossCount+=1
            #if crossCount==crossings:
                #print "crosses!"
                #self.sumV=0
            #time.sleep(.001)
        #print "paso por el voltaje inicial ", crossCount
        #print "samples = ", nSamples
        #print "offsetV", self.offsetV
        #print "lastSample ", self.sampleV
        #print "filteredV ", self.filteredV
                 
        #print "sumV = ", (self.sumV/nSamples)
        #post loop calculations
        if(voltSensor==False):
            self.realPower=0
            self.apparentPower=0
            self.Vrms=0
        else: 
            V_RATIO=self.calibrationV*((SupplyVoltage/1000.0)/self.ADC_COUNTS)
            self.Vrms=V_RATIO*math.sqrt(self.sumV/nSamples)
            #print "Vrms", self.Vrms

            I_RATIO=self.calibrationI*((SupplyVoltage/1000.0)/self.ADC_COUNTS)
            self.Irms=I_RATIO*math.sqrt(self.sumI/nSamples)

            #Calculation power values
            self.realPower=V_RATIO*I_RATIO*self.sumP/nSamples
            self.apparentPower=self.Vrms*self.Irms
        #self.powerFactor=self.realPower/self.apparentPower
            self.powerFactor=self.realPower/self.apparentPower
        print "Vrms = ", self.Vrms
        print "Irms = ", self.Irms
        print "realPower = ", self.realPower
        print "apparentPower = ", self.apparentPower
        print "powerFactor= ", self.powerFactor


        self.sumV=0
        self.sumI=0
        self.sumP=0
        self.filteredV=0
        self.filteredI=0
        return True

#class MCP:#adc
#    def __init__(self):
#        self.SPI_PORT=0
#        self.SPI_DEVICE=0
#        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


