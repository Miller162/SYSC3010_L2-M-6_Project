try: 
    from gpiozero import Button
    import time
    import math
except ImportError:
    print("Import Error")

else: print("Import Successful")


try:

    def sensor_inputs():
       
            North_direction=Button(3)
            North_direction.when_pressed=North

            East_direction=Button(4)
            East_direction.when_pressed=East

            South_direction=Button(14)
            South_direction.when_pressed=South

            West_direction=Button(15)
            West_direction.when_pressed=West
except:
    print("Input error")
else:
    print("Receiving direction inputs successfully")

        

