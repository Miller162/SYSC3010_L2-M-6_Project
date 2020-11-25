""""Motor test script

This script tests that all necessary libraries to properly utilize the motors are able to be imported successfully.
It also ensures that all GPIO pins are able to be successfully setup.
It will then run a test case that causes motor output.  This test case is outlined further in the test function docstring

This file can be imported as a module with the following functions:

    *Motor_test - performs the afformentioned tests on the motor setup and implementation
    *up - causes the motors to roll up
    *down - causes the motore to roll down
"""

#TESTING import statements
try: 
    import RPi.GPIO as GPIO
    
except ImportError:
    print ("GPIO module could not be imported")
    
else:
    print ("GPIO module imported successfully")
    
#END try-except
    
try:
    from time import sleep
    
except ImportError:
    print ("Time module could not be imported")
    
else:
    print ("Time module imported successfully")
#END try-except
    
def down():
    """A function that causes the motors to roll down"""
    print("down")
    GPIO.output(17, GPIO.HIGH) #set input 1 to logic high
    GPIO.output(27, GPIO.LOW) #set input 2 to logic low    
    
    sleep(10)
    
    #reset values to logic low
    GPIO.output(17, GPIO.LOW) 
    GPIO.output(27, GPIO.LOW)
#END clockwise

def up():
    """A function that causes the motors to roll up"""
    print("up")
    GPIO.output(17, GPIO.LOW) #set input 1 to logic low
    GPIO.output(27, GPIO.HIGH) #set input 2 to logic high
    
    sleep(10)
    
    #reset values to logic low
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
#END counter_clockwise

def Motor_test():
    """A function that runs various tests on the initiialization and implementation of the external motors

    This function tests the GPIO pin setup, and runs a script that should cause the motors to roll all the way up and then unroll completely.
    if the GPIO pin setup produces an error the function will indicate that an error occured in that section of the code.
    If the motors do not roll all the way up and then down this indicates that there is a hardware error
    """

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(4, GPIO.OUT) #Motor enable
        GPIO.setup(17, GPIO.OUT) #H-Bridge input 1
        GPIO.setup(27, GPIO.OUT) #H-Bridge input 2
        
    except:
        print ("GPIO setup error")
        
    else:
        print ("GPIO setup successfully")
    #END try-except
    
    #Enable H-bridge output
    GPIO.output(4, GPIO.HIGH)
    
    up()
    sleep(3)
    down()
    
    GPIO.cleanup() #resetting pins to defaults
#END Motor_test
    
#Motor_test()  #for use when run as an individual file. commented out when in use as an importable library in main test file
