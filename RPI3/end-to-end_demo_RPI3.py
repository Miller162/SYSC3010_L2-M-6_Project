from gpiozero import Button
import time
import math
import http.client
import urllib.request
import RPi.GPIO as gpio

#Anemometer
wind_count=0
radius_cm=9.0
wind_interval=4
wind_speed=0
#Wind Vane 
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
reed_switch1=3
reed_switch2=14



gpio.setup(reed_switch1,gpio.IN)
gpio.setup(reed_switch2,gpio.IN)

#determines the direction the wind is blowing 
def determine_direction():
    
    if(gpio.input(reed_switch1)== False):
        direction="NW"
        return direction
        
     
    elif (gpio.input(reed_switch2)== False):
        direction="N"
        return direction
        
    else:     
        direction="No_Wind"
        return direction
        

#----------------------------------------------------------------------------------
#Anemometer: Determinet the wind speed
#Determines the number of spins on the anemometer 
def spin():
    global wind_count
    wind_count=wind_count+1
    print("spin"+str(wind_count))
    
#Converts the number of rotations into speed in cm per second
def calculate_speed(time_sec):
    global wind_count
    circumference_cm=(2*math.pi)*radius_cm
    rotations=wind_count
    
    dist_cm=circumference_cm*rotations
    speed=dist_cm/time_sec
    return speed

wind_speed_sensor=Button(2) #Hall effect sensor indicating the number of rotations
wind_speed_sensor.when_pressed=spin

#This code wrties the data collected from the anemometer and the wind vane to thingspeak 
def write_to_thingspeak(wind_speed,wind_direction):
    URL='http://api.thingspeak.com/update?api_key='
    KEY="FLTQP4SFI3BIHJVN"
    HEADER='&field1={}&field2={}'.format(wind_speed,wind_direction)
    NEW_URL=URL+KEY+HEADER
    print(NEW_URL)
    data=urllib.request.urlopen(NEW_URL)
    print(data)

while True:
    wind_count=0
    time.sleep(wind_interval)
    wind_speed=calculate_speed(wind_interval)
    print(wwind_speed, "cm/h")
    wind_direction=determine_direction()
    print(wind_direction)
    write_to_thingspeak(wind_speed,wind_direction)
    
    


    
