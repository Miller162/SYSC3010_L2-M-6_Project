from gpiozero import Button
import time
import math
import Anemometer_test
import Wind_Vane_Test




def testing():
    Anemometer_test.sensor_input_test()
    Wind_Vane_Test.sensor_inputs()



def North():
    print("North")
def South():
    print("South")
def East():
    print("East")
def West():
    print("West")



North_direction=Button(3)


East_direction=Button(4)


South_direction=Button(14)


West_direction=Button(15)



    
#Anemometer
wind_count=0
radius_m=0.09
wind_interval=4
wind_speed=0
def spin():
    global wind_count
    wind_count=wind_count+1
    print("spin"+str(wind_count))
    
#Converts the number of rotations into speed in cm per second
def calculate_speed(time_sec):
    global wind_count
    circumference_m=(2*math.pi)*radius_m
    rotations=wind_count
    
    dist_m=circumference_m*rotations
    speed=dist_m/time_sec
    return speed

wind_speed_sensor=Button(2) #Hall effect sensor indicating the number of rotations
wind_speed_sensor.when_pressed=spin

while True:
    wind_count=0
    time.sleep(wind_interval)
    wind_speed=calculate_speed(wind_interval)
    North_direction.when_pressed=North
    East_direction.when_pressed=East
    South_direction.when_pressed=South
    West_direction.when_pressed=West
    print(wind_speed, "m/h")