"""
NAME: Gurjit Gill
DATE: November 16, 2020
COURSE: SYSC 3010
DESCRIPTION: The following is a test program that reads and uploads sensor values from the SenseHat to the ThingSpeak channel, effectively demonstrating RPI2's communication protocols.
"""

# Required imports/libraries
from sense_hat import SenseHat
import urllib.request
from time import sleep

# While-loop to allow for multiple data points
while (1):
    sense = SenseHat()
    sense.clear()

    pressure = sense.get_pressure()
    print(pressure)

    temp = sense.get_temperature_from_pressure()
    print(temp)

    humidity = sense.get_humidity()
    print (humidity)

    URL = 'https://api.thingspeak.com/update?api_key='
    KEY = 'JOHC5J4TZM2L3PPF'
    HEADER = '&field1={}&field2={}&field3={}'.format(temp,pressure,humidity)

    new_URL = URL + KEY + HEADER
    #print(new_URL)
    data = urllib.request.urlopen(new_URL)
    print(data)
    
    sleep(4)