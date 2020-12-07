"""
Akkash Anton Amalarajah
Description: This program is the full implementation of the wind devices, the Anemometer and Wind Vane. This progrm
controls RPI3 which then collects the data from the wind devices and converts them to wind speed and wind direction
and sends the results to thingspeak. The program also runs test cases to pass to ensure the devices are fully functional
The program counts the number of rotations on the anemometer and converts the RPM to speed based on the variables.
For wind direction, the program detects which sensor is triggered on the wind vane and outputs the coresponding
direction value. Both devices update every 60 seconds. 
"""
#Import required libraries and classes
from gpiozero import Button#Button class imported from gpiozero Library
import RPi.GPIO as gpio # importing GPIO pins from Raspberry pi
import time # time class imported
import math # math class that is used for conversion 
import http.client # http library used to write ot thingspeak
import urllib.request #url library used to write to thingspeak
import RPI3_Anemometer_test #Test class to test anemometer 
import RPI3_Wind_Vane_test #Test class to test wind vane

#----------------------------------------------------------------------------------
#Test function that runs the tests from other class
def testing():
    sensor_input_test()
    sleep(1)
    speed_conversion_test()
    direction_sensor_inputs()
    anemometer_input_test()
    
#Anemometer
    
rotations=0# counts the number of rotations from the anemoemter 
radius_cm=14.25 # the radius of the anemoemeter used to determine the speed 
interval=5 # the time in seconds of how often the readings are outputted
wind_speed=0 # the initial speed of the wind set to 0

#Wind Vane

#Each sensor is associated with a specific direction. 
North_direction=Button(2)#North Direction is connected to the sensor using GPIO pin 3
East_direction=Button(4)#East Direction is connected to the sensor using GPIO pin 3
South_direction=Button(27)#South Direction is connected to the sensor using GPIO pin 14
West_direction=Button(10)#West Direction is connected to the sensor using GPIO pin 15
Northwest_direction=Button(11)#North West Direction is connected to the sensor using GPIO pin 11
SouthWest_direction=Button(22)#South West Direction is connected to the sensor using GPIO pin 22
NorthEast_direction=Button(3)#North East Direction is connected to the sensor using GPIO pin 3
SouthEast_direction=Button(14)#South East Direction is connected to the sensor using GPIO pin 17

# Wind Vane: Determine direction wind is flowing in
# The following block of code is run to see which sensor is currently active and assigns the assigned direction.


def direction():
    #If the North sensor is active, then the directin is North. 
    if (North_direction.is_pressed==True):
        direction="North"
        return direction
    #If the South sensor is active, then the direction is South. 
    elif (South_direction.is_pressed==True):
        direction="South"
        return direction
    #If the West sensor is active, then the direction is West. 
    elif (West_direction.is_pressed==True):
        direction="West"
        return direction
    #If the East sensor is active, then the direction is East. 
    elif(Northwest_direction.is_pressed==True):
        direction="North_West"
        return direction
    #If the South West sensor is active, then the direction is South West
    elif(SouthWest_direction.is_pressed==True):
        direction="South_West"
        return direction
    #If the North East sensor is active, then the direction is North East
    elif(NorthEast_direction.is_pressed==True):
        direction="North_East"
        return direction
    #If the South East sensor is active, then the direction is South East
    elif(SouthEast_direction.is_pressed==True):
        direction="South_East"
        return direction
    #If the East sensor is active, then the direction is East
    elif(East_direction.is_pressed==True):
        direction="East"
        return direction
    #If no sensor is active at that time
    else:
        return None
#----------------------------------------------------------------------------------
#Anemometer
#Anemometer: Determine the wind speed

#Determines the number of spins on the anemometer
def spin():
    global rotations
    rotations=rotations+1
    print("Rotation"+str(rotations))#prints the number of spin outputs
    
#Converts the number of rotations into speed in km per hour
def calculate_speed(time_seconds):
    global rotations
    circumference_cm=(2*math.pi)*radius_cm
    rotations=rotations
    
    dist_cm=circumference_cm*rotations
    speed=dist_cm/time_seconds
    #The code below converts the speed from cm/sec to km/h
    distance_km=(circumference_cm*rotations)/100000
    km_per_hour=(distance_km/time_seconds)*3600
    return km_per_hour

wind_speed_sensor=Button(17) #Hall effect sensor indicating the number of rotations
wind_speed_sensor.when_pressed=spin#When the sensor is triggered it triggers the spin function

#This code wrties the data collected from the anemometer and the wind vane to thingspeak 
def write_to_thingspeak(wind_speed,wind_direction):
    URL='http://api.thingspeak.com/update?api_key='
    KEY="FLTQP4SFI3BIHJVN"
    HEADER='&field1={}&field2={}'.format(wind_speed,wind_direction)
    NEW_URL=URL+KEY+HEADER
    print(NEW_URL)
    data=urllib.request.urlopen(NEW_URL)
    print(data)
#While loop to run the system to get the live direction at all times. Direction is updated every 5 seconds. It also
#runs the anemometer on the wind count interval. This while loop also writes the final wind speed and wind direction
#to thingspeak. 
while True:
    rotations=0
    time.sleep(interval)
    wind_speed=calculate_speed(interval)
    print(wind_speed, "km/h")#print the wind speed
    wind_direction=direction()
    print(direction())#print the current direction
    #time.sleep(1)#update every 1 second 
    write_to_thingspeak(wind_speed,wind_direction)#write to thingspeak
    
    


    

