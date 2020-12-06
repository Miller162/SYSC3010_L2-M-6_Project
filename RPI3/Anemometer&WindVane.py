from gpiozero import Button#Button class imported from gpiozero Library
import RPi.GPIO as gpio # importing GPIO pins from Raspberry pi
import time # time class imported
import math # math class that is used for conversion 
import http.client # http library used to write ot thingspeak
import urllib.request #url library used to write to thingspeak

#----------------------------------------------------------------------------------
#Anemometer
wind_count=0# counts the number of rotations from the anemoemter 
radius_cm=0.0001425 # the radius of the anemoemeter used to determine the speed 
wind_interval=60 # the time in seconds of how often the readings are outputted
wind_speed=0 # the speed of the wind 

#Wind Vane
#Each sensor is associated with a specific direction. 
North_direction=Button(3)#North Direction is connected to the sensor using GPIO pin 3
East_direction=Button(4)#East Direction is connected to the sensor using GPIO pin 3
South_direction=Button(17)#South Direction is connected to the sensor using GPIO pin 14
West_direction=Button(27)#West Direction is connected to the sensor using GPIO pin 15
Northwest_direction=Button(22)
SouthWest_direction=Button(10)
NorthEast_direction=Button(9)
SouthEast_direction=Button(2)

#Wind Vane: Determine direction wind is flowing in
# The following block of code is run to see which sensor is currently active and assigns the assigned direction.


def direction():
    #If the North sensor is active, then the directin is North. 
    if (North_direction.is_pressed==True):
        direction="North"
        return direction
    #If the South sensor is active, then the directin is South. 
    elif (South_direction.is_pressed==True):
        direction="South"
        return direction
    #If the West sensor is active, then the directin is West. 
    elif (West_direction.is_pressed==True):
        direction="West"
        return direction
    #If the East sensor is active, then the directin is East. 
    elif(Northwest_direction.is_pressed==True):
        direction="North_West"
        return direction
    elif(SouthWest_direction.is_pressed==True):
        direction="South_West"
        return direction
    elif(NorthEast_direction.is_pressed==True):
        direction="North_East"
        return direction
    elif(SouthEast_direction.is_pressed==True):
        direction="South_East"
        return direction
    elif(East_direction.is_pressed==True):
        direction="East"
        return direction
    #If no sensor is active. This is only when the system is initialized. Otherwise the system will always have a direction
    else:
        return None
#----------------------------------------------------------------------------------
#Anemometer
#Anemometer: Determine the wind speed

#Determines the number of spins on the anemometer
def spin():
    global wind_count
    wind_count=wind_count+1
    print("spin"+str(wind_count))#prints the number of spin outputs
    
#Converts the number of rotations into speed in cm per second
def calculate_speed(time_sec):
    global wind_count
    circumference_cm=(2*math.pi)*radius_cm
    rotations=wind_count
    
    dist_cm=circumference_cm*rotations
    speed=dist_cm/time_sec
    return speed

wind_speed_sensor=Button(14) #Hall effect sensor indicating the number of rotations
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
    wind_count=0
    time.sleep(wind_interval)
    wind_speed=calculate_speed(wind_interval)
    print(wind_speed, "km/h")#print the wind speed
    wind_direction=direction()
    print(direction())#print the current direction
    time.sleep(1)#update every 1 second 
    write_to_thingspeak(wind_speed,wind_direction)#write to thingspeak
    
    


    


