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

#LED_test()