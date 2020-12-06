"""
NAME: Gurjit Gill
DATE: November 16, 2020
COURSE: SYSC 3010
DESCRIPTION: The following is a test program that reads and uploads sensor values from the SenseHat to the ThingSpeak channel, effectively demonstrating RPI2's communication
                protocols. This class was used for testing purposes, experimented with different ideas and code here. 
"""

# Required imports/libraries
from sense_hat import SenseHat
import urllib.request
from time import sleep
from gpiozero import CPUTemperature
import os

# This function will determine the current cpu temperature as a float
def get_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    t = float(res.replace("temp=","").replace("'C\n",""))
    return(t)

# While-loop to allow for multiple data points
while (1):
    sense = SenseHat()
    sense.clear()

    pressure = sense.get_pressure()
    print(pressure)
    
    cpuTemp = get_cpu_temp()
    #cpuTemp = float(cpuTemp.replace("gpiozero.CPUTemperature",""))
    print(cpuTemp)
    temp = sense.get_temperature_from_pressure()
    #print(temp)
    
    actualTemp = temp - ((temp - cpuTemp)/1.5)  #Worked on creating this algorithm to create an accurate temperature reading that accounts for the on-board cpu temperature
    print(actualTemp)

    humidity = sense.get_humidity()
    print (humidity)
    
    sleep(4)
