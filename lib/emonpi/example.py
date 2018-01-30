#!/usr/bin python
from Emonlib import EnergyMonitor as EnergyMonitor




if __name__ == "__main__":
    myEnergy=EnergyMonitor()
    myEnergy.setVoltage(0, 1230, 1.7)
    myEnergy.setCurrent(1, 90.9)
    myEnergy.calcVI(20, 2)

