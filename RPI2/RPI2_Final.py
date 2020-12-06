"""
NAME: Gurjit Gill
DATE: November 16, 2020
COURSE: SYSC 3010
Description: The following program is the final edition for RPI2 of the HEMAS system. The purpose of this RPi is collecting environmental data and uploading it to the
                thingspeak channel, making it readily available to the other RPis, the database and its graphical user interface. The variables that this RPi will be
                collecting are temperature (C), pressure (millibars), humiditity (%), and seismic activity (magnitude on the Richter scale). The program is setup to
                collect data every second. The temperature value is altered with an algorithm to account for the on-board cpu temperature that would have deviated our
                measurements for the room temperature. Seismic activity from magnitudes 1-4 are displayed as undetected as they are hard to differentiate and are not
                capable of damage to a home. Magnitudes 10-12 are labelled as '10+' as they also have minimal difference among them in terms of peak acceleration in
                (m/s^2) or g-force.
"""

# Required imports/libraries
from sense_hat import SenseHat
import urllib.request
from time import sleep
from gpiozero import CPUTemperature
import time

red = (255, 0, 0)    #Pre-defining the rgb values for these 2 colors to be used on the SenseHat LED Matrix
blue = (0, 0, 255)

sense = SenseHat()

# The following function is responsible for conducting all of the environmental data collection. It will obtain the values and return them in four seperate variables.
def get_data():
    sense = SenseHat() #initialize the SenseHat to the variable 'sense'
    sense.clear() #Clears any previous action on the SenseHat

    pressure = sense.get_pressure()               #Obtain a pressure value using the on-board pressure sensor
    print("Pressure: ", pressure, "millibars")       #Print the value in the shell, purely for visualization and testing purposes for the developers

    cpuTemp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3    #Obtain a CPU temperature value, averages around 50 degrees celcius which offsets room
    #print(cpuTemp)                                                              #temperature readings
    
    temp = sense.get_temperature_from_pressure()   #Obtain a room temperature value using the on-board pressure sensor
    temp = temp-((cpuTemp-temp)/1.5)             #Found this conversion to work best to account for the CPU temperature
    print("Temperature: ", temp, " Celcius")    #At this point the 'temp' variable now contains the new temperature value that we have calculated in the line above

    humidity = sense.get_humidity()         #Obtain a humidity value using the on-board humidity sensor
    print ("Humidity: " , humidity, "%")    #Also prints it in shell

    x, y, z = sense.get_accelerometer_raw().values()     #Obtains acceleration values in G-force (G) for each 3-dimensional axis

    x = abs(x)   # This allows for the absoulute value of the readings to be saved
    y = abs(y)   # For the purposes of this project, do not need any directions or negative values. Simply require just the magnitude of the readings.
    z = abs(z)

    if x > 1.24 or y > 1.24:
        magnitude = "10+"
    elif x > 0.65 or y > 0.65:
        magnitude = "9"
    elif x > 0.34 or y > 0.34:          # This block of if and elif statements designate a Richter-scale magnitude depending on the peak-accleration measured by the
        magnitude = "8"                 # accelerometer. As previously stated, magnitudes below are deemed irrelevant due to its low risk factor and the complexity of
    elif x > 0.18 or y > 0.18:          # differentiating between those magnitdues. Sam goes for magnitudes 10-12 and are thus labelled as 10+.
        magnitude = "7"
    elif x > 0.092 or y > 0.092:
        magnitude = "6"
    elif x > 0.039 or y > 0.039:
        magnitude = "5"
    else:
        magnitude = "Undetected"
    
    print ("Magnitude: " , magnitude)  #prints in the shell for testing-purposes
    
    return  temp, pressure, humidity, magnitude    #Returns all of the values measured/ calculated into these variables

# The following function is setup to write the data to my thingSpeak channel into four spearate fields. This allows for it to be readily available for the database.
def write_to_thingspeak(temp, pressure, humidity, magnitude):     # Takes the four data variables as input
    
    URL = 'https://api.thingspeak.com/update?api_key='   #Setting up the write channel, first part of the URL
    KEY = 'JOHC5J4TZM2L3PPF'                       # My write key for adding to the channel
    HEADER = '&field1={}&field2={}&field3={}&field4={}'.format(temp,pressure,humidity,magnitude)  #Setting up the header to pair each field with its own variable

    new_URL = URL + KEY + HEADER           #Creating the complete URL by combining all of the parts
    data = urllib.request.urlopen(new_URL)

    print(data)

# This is the code outside of any function. This while-loop will run endlessly to make sure contant data collection occurs.
while (1):
    
    temp, pressure, humidity, magnitude = get_data()     # Calls the get_data() fucntion and sets up the four variables for it to be stored into.

    write_to_thingspeak(temp, pressure, humidity, magnitude)   # Calls the write_to_thingspeak function while sending it the four data vairables
    
    pixels = [red if i < humidity else blue for i in range(64)]   #Sets up an LED matrix display dependent on the humidity value
    sense.set_pixels(pixels)

    sleep(1) # This is a buffer that allows for easy control over the frequency of our data collection. At this moment it is set-up to run the while-loop again after one second.
