try: 
    from gpiozero import Button
    import time
    import math
except ImportError:
    print("Import Error")

else:
    print("Import Successful")

wind_count=0
radius_m=0.09
wind_interval=4
wind_speed=0
try:
    def sensor_input_test():
        
            wind_speed_sensor=Button(2)
            wind_speed_sensor.when_pressed=spin
        
except:
    print("No inputs received")
else:
    print("Anemometer inputs received")

try:
    def speed_conversion_test():
        
            global wind_count
            circumference_m=(2*math.pi)*radius_m
            rotations=wind_count
            
            dist_m=circumference_m*rotations
            speed=dist_m/time_sec
            return speed
except:
    print("Speed was not calcualted")
else:
    print("Speed calculated succesfully")

            


