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
    #def __init__(self, fileName):
     #   self.readConfigFile(fileName)
        
    #constructor for battery without reading from config file    
    def __init__(self, currentCapacity, maxCapacity, load):
        self.__currentCapacity = currentCapacity
        self.__maxCapacity = maxCapacity
        self.__load = load
    
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
        return (f'Max Capacity: {self.__maxCapacity} J\nCurrent Capacity: {self.__currentCapacity} J\nLoad: {self.__load}')
        
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
        f = open(fileName, "r")
        inc = 0
        fail = 0
        lasttime = 0
        time = 0
        time_list = []
        capacity_list = []
        
        for i in range(start, end):
            data = lc.getline(fileName, i).split()
            lasttime = time
            time = int(data[0])
            irr = float(data[1])
            energy = self.convert(irr, self.AREA_OF_SENSOR, time-lasttime)
            inc_or_fail = self.loadBattery(energy, self.__load * (time-lasttime))
            if (inc_or_fail == 1):
                inc+=1
            if (inc_or_fail == -1):
                fail+=1
            time_list.append(time)
            capacity_list.append(self.__currentCapacity)    
        f.close()
        
        time_axis = [time_list[i] for i in range(len(time_list)) if i % 3600 == 0]
        capacity_axis = [capacity_list[i] for i in range(len(capacity_list)) if i % 3600 == 0]
        print("Stored",inc,"times out of",end-start,"% is",inc/(end-start))
        print("Failed",fail,"times out of",end-start,"% is",fail/(end-start))
        plt.scatter(time_axis, capacity_axis)
        plt.xlabel('Time(sec)')
        plt.ylabel('Battery Capacity(J)')
        
        graph_name = input("input filename\n")
        plt.savefig(graph_name)
 
        plt.show()        
        
        '''save = input("save? y or n")
        
        if(save == "y"):
            graph_name = input()
            plt.savefig(graph_name)
        else:
            print('oof')'''
    
    #convert irradiance to Joules. 
    def convert(self, irrad, area, time):
        return irrad * area * time
    
battery100 = Battery(0, 1000, 0.001)
battery500 = Battery(0, 1000, 0.005)
battery1000 = Battery(0, 1000, 0.01)
battery2500 = Battery(0, 1000, 0.05)

print(battery100)
battery100.readFileRange("SetupD.txt", 2 , 900002)
print(battery500)
battery500.readFileRange("SetupD.txt", 2 , 900002)
print(battery1000)
battery1000.readFileRange("SetupD.txt", 2 , 900002)
print(battery2500)
battery2500.readFileRange("SetupD.txt", 2 , 900002)


