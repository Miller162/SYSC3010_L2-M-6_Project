#Test code to see if the wind vane program is working

try: 
    from gpiozero import Button
    import time
    import math
except ImportError:
    print("Import Error")

else: print("Import Successful")


try:

    def direction_sensor_inputs():
       
            North_direction=Button(2)
            North_East_direction=Button(3)
            East_direction=Button(4)
            South_East_direction=Button(17)
            South_direction=Button(27)
            South_West_direction=Button(22)
            West_direction=Button(10)
            North_West_direction=Button(9)
           
except:
    print("Input error")
else:
    print("Receiving direction inputs successfully")

        

