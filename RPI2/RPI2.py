"""
NAME: Gurjit Gill
DATE: November 16, 2020
COURSE: SYSC 3010
"""

# Required imports/libraries
from sense_hat import SenseHat
import urllib.request
from time import sleep
from gpiozero import CPUTemperature

red = (255, 0, 0)
blue = (0, 0, 255)

# While-loop to allow for multiple data points
while (1):
    sense = SenseHat()
    sense.clear()

    pressure = sense.get_pressure()
    print("Pressure: ", pressure, "millibars")
    
    cpuTemp = CPUTemperature()
    #print(cpuTemp)
    temp = sense.get_temperature_from_pressure()
    temp = temp/1.5
    print("Temperature: ", temp, " Celcius")

    humidity = sense.get_humidity()
    print ("Humidity: " , humidity, "%")
    
    pixels = [red if i < humidity else blue for i in range(64)]
    sense.set_pixels(pixels)

    URL = 'https://api.thingspeak.com/update?api_key='
    KEY = 'JOHC5J4TZM2L3PPF'
    HEADER = '&field1={}&field2={}&field3={}'.format(temp,pressure,humidity)

    new_URL = URL + KEY + HEADER
    #print(new_URL)
    data = urllib.request.urlopen(new_URL)
    
    print(data)
    
    sleep(4)
