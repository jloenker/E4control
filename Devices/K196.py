#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DEVICE import DEVICE
import math

class K196:
    dv = None
    mode = None

    def __init__(self,kind,adress,port):
        self.dv = DEVICE(kind=kind, adress=adress, port=port)

    def userCmd(self,cmd):
    	print "userCmd: %s" % cmd
    	return self.dv.ask(cmd)

    def initialize(self, sMode):
        if (sMode == "H"):
            self.setKind("DCV")
            self.setRange("RO")
            self.mode = "H"
            pass
        elif (sMode == "T"):
            self.setKind("OHM")
            self.setRange("R2")
            self.mode = "T"
            pass
        elif (sMode == "V"):
            self.setKind("DCV")
            self.setRange("R0")
            self.mode = "V"
            pass
        else:
             print("Initializing not possible: Unknown mode!")
        pass

    def setKind(self, sKind):
        if (sKind == "DCV"): self.dv.write("F0X")
        elif (sKind == "ACV"): self.dv.write("F1X")
        elif (sKind == "OHM"): self.dv.write("F2X")
        elif (sKind == "OCO"): self.dv.write("F7X")
        elif (sKind == "DCI"): self.dv.write("F3X")
        elif (sKind == "ACI"): self.dv.write("F4X")
        elif (sKind == "dBV"): self.dv.write("F5X")
        elif (sKind == "dBI"): self.dv.write("F6X")
        pass

    def getStatus(self):
        return self.dv.ask("U0X")

    def getKind(self):
        s = self.dv.read()
        return s[0:4]

    def getValue(self,channel=-1):
        v = self.dv.read()
        return float(v[4:16])

    def getTempPT100(self,channel=-1):
        a = 3.90802E-3
        b = -5.802E-7
        R0 = 100.00
        R = self.getValue()
        if R > 10000000: return(9999)
        return (-a/(2*b)-math.sqrt(R/(R0*b)-1/b+(a/(2*b))*(a/(2*b))))

    def getTempPT1000(self,channel=-1):
        a = 3.90802E-3
        b = -5.802E-7
        R0 = 1000.00
        R = self.getValue()
        if R > 10000000: return(9999)
        return (-a/(2*b)-math.sqrt(R/(R0*b)-1/b+(a/(2*b))*(a/(2*b))))

    def getHumidity(self, fTemp,channel=-1):
        a=0.0315
        b=0.826
        V = self.getValue()
        return ((V-b)/a)/(1.0546-0.00216*fTemp);

    def getVoltage(self, channel=-1):
        V = self.getValue()
        return(V)

    def setRange(self,sRange):
        if (sRange == "R0") : self.dv.write("R0X")
        elif (sRange == "R1") : self.dv.write("R1X")
        elif (sRange == "R2") : self.dv.write("R2X")
        elif (sRange == "R3") : self.dv.write("R3X")
        elif (sRange == "R4") : self.dv.write("R4X")
        elif (sRange == "R5") : self.dv.write("R5X")
        elif (sRange == "R6") : self.dv.write("R6X")
        elif (sRange == "R7") : self.dv.write("R7X")
        pass

    def writeOnDisplay(self, sMsg):
        msg = "D" + sMsg + "X"
        if (len(sMsg) <= 10): self.dv.write(msg)
        else: print("Message to long!")
        pass

    def restart(self):
        self.dv.write("L0X")
        pass

    def close(self):
        self.dv.close()
        pass


    def output(self, sMode=mode,  show = True):
        if show:
            print("K196:")
        values = []
        header = []
        if (sMode == "H"):
            fHumidity = self.getVoltage()
            if show:
                print("Humidity = %0.4f V"%fHumidity)
            values.append(str(fHumidity))
            header.append("H[V]")
        elif (sMode == "T"):
            fResistance = self.getResistance()
            fTemperature = self.getTempPT1000()
            values.append(str(fResistance))
            header.append("R%i[Ohm]"%i)
            values.append(str(fTemperature))
            header.append("T%i[C]"%i)
            if show:
                print("values:"+"\t"+"%.2f Ohm"%fResistance + "\t" + "%.1f °C"%fTemperature)
        elif (sMode == "V"):
            fVoltage = self.getVoltage()
            values.append(str(fVoltage))
            header.append("U[V]")
            if show:
                print("Voltage = %0.4f V"%fVoltage)
        else:
            print("Error!")
        return([header,values])

    def interaction(self):
        print("Nothing to do...")