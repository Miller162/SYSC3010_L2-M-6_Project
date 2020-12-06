from sense_hat import SenseHat
import time

while (1):
    sense = SenseHat()

    sense.clear()

    x, y, z = sense.get_accelerometer_raw().values()
    
    x = abs(x)
    y = abs(y)
    z = abs(z)
    
    print (x, y, z)