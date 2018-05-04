#!/usr/bin python

def saveKw(kwH, myDatabase, httpCom):#
    print "\n"
    print "\n"
    print "kw/h = ", kwH[0]
    xmlPower=httpCom.createXml(kwH[0])#the xml is created then is saved in the database
    print "kw/h xml = ",xmlPower
    myDatabase.insertXml(xmlPower)
    #print "emonVec", emonVec.

def settleReadings(emonVec):
    numSamples=20
    for i in range(numSamples):
        for emon in emonVec:#all the power phases
            emon.calcVI(50, 5, True)
            #print "emon power = ", emon.realPower

