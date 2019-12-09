# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 16:05:31 2019

@author: blarg
"""

import numpy as np
import linecache as lc
import matplotlib.pyplot as plt

class Battery:
    AREA_OF_SENSOR = 0.15 #in square millimeters

    #constructor for battery
    def __init__(self, fileName):
        self.readConfigFile(fileName)
    
    #constructor for battery without reading from config file
    def setProperties(self, currentCapacity, maxCapacity, load):
        self.currentCapacity = currentCapacity
        self.maxCapacity = maxCapacity
        self.load = load
    
    #reads from config file and sets the values to the object attributes   
    def readConfigFile(self, fileName):
        file = open(fileName, "r")
        input = file.readlines()
        
        for line in input:
            data = line.split()
            
            name = data[0]
            value = data[2]
            
            if(name.lower() == "currentcapacity"):    
                self.__currentCapacity = float(value)
            elif(name.lower() == "maxcapacity"):
                self.__maxCapacity = float(value)
            elif(name.lower() == "load"):
                self.__load = float(value)
        file.close()
    
    #getters and setters
    @property
    def currentCapacity(self):
        return self.__currentCapacity
    
    @currentCapacity.setter
    def currentCapacity(self, value):
        self.__currentCapacity = value
        
    @property
    def maxCapacity(self, value):
        return self.__currentCapacity
    
    @maxCapacity.setter
    def maxCapacity(self, value):
        self.__maxCapacity = value
    
    def __str__(self):
        return (f'Max Capacity: {self.__maxCapacity} J\nCurrent Capacity: {self.__currentCapacity} J')
        
    def __repr__(self):
        return (f'{self.__class__.__name__}({self.__energyHarvested!r}')
    
    #computes the current capacity of the battery based of the parameters energyHarvested and energyOfLoad.
    def loadBattery(self, energyHarvested, energyOfLoad):
        
        energyStored = energyHarvested - energyOfLoad
        
        if(energyStored > 0):
            if(energyStored + self.__currentCapacity > self.__maxCapacity):
                self.__currentCapacity = self.__maxCapacity
            else:
                self.__currentCapacity += energyStored
            return 1
        elif(energyStored < 0):
            if(energyStored + self.__currentCapacity < 0):
                self.currentCapacity = 0
                return -1
            else:
                self.__currentCapacity += energyStored
            return 0
                
    #86370 = 1day
    #reads the file from a range of line numbers
    def readFileRange(self, fileName, start, end):
        inc = 0
        fail = 0
        t = []
        d = []
        f = open(fileName, "r")
        lasttime = 0
        time = 0
        for i in range(start, end):
        #for i in f:
            data = lc.getline(fileName, i).split()
            lasttime = time
            time = int(data[0])
            irr = float(data[1])
            energy = self.convert(irr, self.AREA_OF_SENSOR, time-lasttime)
            q = self.loadBattery(energy, self.__load * (time-lasttime))
            if (q == 1):
                inc+=1
            if (q == -1):
                fail+=1
            t.append(time)
            d.append(self.__currentCapacity)
            #data.append(lc.getline(fileName, i).split()[1])
            #print(self.__currentCapacity)
        f.close()
        #print(t)
        #print(d)
        #print(len(t), len(d))
        t2 = [t[i] for i in range(len(t)) if i % 3600 == 0]
        d2 = [d[i] for i in range(len(d)) if i % 3600 == 0]
        print("Stored",inc,"times out of",end-start,"% is",inc/(end-start))
        print("Failed",fail,"times out of",end-start,"% is",fail/(end-start))
        plt.scatter(t2, d2)
        plt.show()

    #def readFileEntire(self, fileName) 
    
    #will convert irradiance to mW-h?
    def convert(self, irrad, area, time):
        return irrad * area * time
    
battery = Battery("battery_Config.txt")
#arbitrary values
print(battery)
#irradiance data from line 2 to 100
battery.readFileRange("SetupC.txt", 1 , 1000001)


