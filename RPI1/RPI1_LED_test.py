""""LED test script

This script tests that all necessary libraries to properly utilize the LED are able to be imported successfully.
It also ensures that all GPIO pins are able to be successfully setup.
It will then run a test case that should cause a specific output on the LED.  This test case is outlined further in the fucntion docstring.

This file can be imported as a module with the following functions:

    *LED_test - performs the afformentioned tests on the LED setup and implementation
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
def LED_test():
    """A function that runs various tests on the initialization and implementation of the external LED

    This function tests the GPIO pin setup, and runs a script using a for loop that should cause the LED to flash 5 times.
    If the GPIO pin setup produces an error the function will indicate that an error occured in that section of the code.
    If the LED does not flash 5 times this indicates there is a hardware issue.
    """
    try: 
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(18, GPIO.OUT)
        
    except:
        print ("GPIO setup error")
        
    else:
        print ("GPIO setup successfully")
    #END try-except
        
    try:
        for _ in range(5): #Flash LED 5 times
            print("LED on")
            GPIO.output(18, GPIO.HIGH) #Turn on LED

            sleep(1) 

            print("LED off")
            GPIO.output(18, GPIO.LOW) #Turn off LED
            
            sleep(1)

        GPIO.cleanup() #Resetting all pins to defaults
        
    except:
        print ("Critical error")
        
    else:
        print ("Program run successfully")
    #END try-except
#END LED_test        

#LED_test() #for use when run as an individual file. commented out when in use as an importable library in main test file
