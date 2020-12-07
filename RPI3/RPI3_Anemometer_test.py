#This code is to test the Anemometer. IT tests if the input is received and if the input is converted to speed
try: 
    from gpiozero import Button
    import time
    import math
except ImportError:
    print("Import Error")

else:
    print("Import Successful")

rotations=0# counts the number of rotations from the anemoemter 
radius_km=0.0001425 # the radius of the anemoemeter used to determine the speed 
interval=10 # the time in seconds of how often the readings are outputted
wind_speed=0 # the initial speed of the wind set to 0
try:
    def anemometer_input_test():
        
            wind_speed_sensor=Button(14)
            wind_speed_sensor.when_pressed=spin
        
except:
    print("No inputs received")
else:
    print("Anemometer inputs received")

try:
    def speed_conversion_test():
        global rotations
        circumference_km=(2*math.pi)*radius_km
        rotations=rotations
    
        dist_km=circumference_km*rotations
        speed=dist_km/time_hours
        return speed
except:
    print("Speed was not calcualted")
else:
    print("Speed calculated succesfully")

            


