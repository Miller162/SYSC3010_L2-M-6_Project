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
def clockwise():
    print("clockwise")
    GPIO.output(17, GPIO.HIGH) #set input 1 to logic high
    GPIO.output(27, GPIO.LOW) #set input 2 to logic low    
    
    sleep(5)
    
    #reset values to logic low
    GPIO.output(17, GPIO.LOW) 
    GPIO.output(27, GPIO.LOW)
#END clockwise

def counter_clockwise():
    print("counter-clockwise")
    GPIO.output(17, GPIO.LOW) #set input 1 to logic low
    GPIO.output(27, GPIO.HIGH) #set input 2 to logic high
    
    sleep(5)
    
    #reset values to logic low
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
#END counter_clockwise

def Motor_test():
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
    
    #Enable motors
    GPIO.output(4, GPIO.HIGH)

    clockwise()
    counter_clockwise()

    GPIO.cleanup() #resetting pins to defaults
#END Motor_test
    
#Motor_test()