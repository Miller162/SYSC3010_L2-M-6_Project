""""Raspberry Pi 1 script

This script will perform all the device tasks, including communicating with ThingSpeak, and all peripheral devices.
The overall purpose of this script is to calculate the lumenance of the area the Raspberry Pi is located in, send that data to a Thingspeak channel,
then read values from a ThingSpeak channel and turn on a light or open blinds depending on those values.

This file can be imported as a module with the following functions:

    *debug - A function that allows for easy printing of statements for debugging
    *testing - A function that runs test cases for the peripherals that have been imported from external files
    *current_average_luma - A function that captures an image via the Pi Camera and calculates the average lumenance of that image
    *write_to_thingspeak - A function that writes the average lumenance data from ThingSpeak
    *search_for_nums - A function that searches for the most recent input from a list of thingspeak data entries
    *read_from_thingspeak - A function that searches for the most recent entry in the desired field of a desired thingspeak channel
    *read_light_status_from_thingspeak - A function that searches for the most recent entry in the light status field of a thingspeak channel
    *read_blinds_status_from_thingspeak - A function that searches for the most recent entry in the light status field of a thingspeak channel
    *motor_up - A function that causes the motors to roll up
    *motor_down - A function that causes the motors to roll down
    *motor_stop - A function that stops the motor rotation
    *LED_init - A function that initializes the LED GPIO pin
    *motor_init - A function that initializes the motor GPIO pins
    *camera_init - A function that initializes a global camera object
    *peripherals_init - A function that calls the initlization functions of the peripheral devices
    *LED_on - A fucntion that turns the LED on
    *LED_of - A fucntion that turns the LED off
    *check_light - A fucntion that checks if there has been a change in the light_status variable, and if so calls the appropriate functions to perform the desired action
    *check_blinds - A fucntion that checks if there has been a change in the blinds_status variable, and if so creates a concurrent thread to perform the desired action
"""
#Imports------------------------------------------------------------------------
def debug(phrase):
    """A function that allows for easy printing of statements for debugging

        Param phrase: the phrased to be printed during debug
    """
    DEBUG = True #turn to True to get debugging print statements
    
    if (DEBUG): #if debug is active
        print(phrase)
    #END if
#END debug

try:
    import RPi.GPIO as GPIO
except ImportError:
    debug("GPIO module could not be imported")
else:
    debug("GPIO module imported successfully")
#END try-except

try:
    from time import sleep
except ImportError:
    debug("Time module could not be imported")
else:
    debug("Time module imported successfully")
#END try-except

try:
    import urllib.request
except ImportError:
    debug("URL LIbray module could not be imported")
else:
    debug("URL LIbray module imported successfully")
#END try-except

try:
    import requests
except ImportError:
    debug("Requests Libray module could not be imported")
else:
    debug("Requests Libray module imported successfully")
#END try-except

try:
    from PIL import Image
except ImportError:
    debug("PIL module could not be imported")
else:
    debug("PIL module imported successfully")
#END try-except

try:
    from picamera import PiCamera
except ImportError:
    debug("Pi Camera test module could not be imported")
else:
    debug("Pi Camera test module imported successfully")
#END try-except

try:
    import json
except ImportError:
    debug("JSON module could not be imported")
else:
    debug("JSON module imported successfully")
#END try-except

try:
    import RPI1_LED_test
except ImportError:
    debug("LED test module could not be imported")
else:
    debug("LED test module imported successfully")
#END try-except

try:
    import RPI1_PiCam_test
except ImportError:
    debug("Pi Camera test module could not be imported")
else:
    debug("Pi Camera test module imported successfully")
#END try-except

try:
    import RPI1_Motor_test
except ImportError:
    debug("Motor test module could not be imported")
else:
    debug("Motor test module imported successfully")
#END try-except

try:
    from threading import Thread, Lock
except ImportError:
    debug("Threading module could not be imported")
else:
    debug("Threading module imported successfully")
#END try-except
    

#functions----------------------------------------------------------------------
def testing():
    """A function that runs test cases for the peripherals that have been imported from external files"""
    RPI1_LED_test.LED_test()
    sleep(1)
    RPI1_PiCam_test.PiCam_test()
    sleep(1)
    RPI1_Motor_test.motor_test()
    sleep(1)

    GPIO.cleanup()
#END testing


def current_average_luma():
    """A function that captures an image via the Pi Camera and calculates the average lumenance of that image"""
    camera.capture('/home/pi/Desktop/image1.jpg') #cameras take picture
    img = Image.open("/home/pi/Desktop/image1.jpg") #opens image

    luma=0 #sum of the lumenance of each pixels
    pixels = img.width*img.height #number of pixels

    for x in range(img.width):
        for y in range(img.height):
            (r, g, b) = img.getpixel((x,y)) #get colour touple
            luma += (0.2126*r + 0.7152*g + 0.0722*b) #calculate realtive luma of RGB data, then add to total
        #END for
    #END for

    img.close() #ensure to properly close the image
    return luma/pixels #return average of all pixels
#END average_luma


def write_to_thingspeak(luma):
    """A function that writes the average lumenance data from ThingSpeak

        Param luma: the average relative lumenance value to be written to ThingSpeak
    """
    URl='https://api.thingspeak.com/update?api_key='
    KEY='VDHAE4N7ZXBU5P5K'
    HEADER='&field1={}'.format(luma)
    NEW_URL=URl+KEY+HEADER

    try:
        urllib.request.urlopen(NEW_URL)
    except:
        debug("Error writing to ThingSpeak")
    else:
        debug("Successfully written to ThingSpeak")
    #END try-except
#END sent_to_thingspeak


def search_for_nums(data):
    """A function that searches for the most recent input from a list of thingspeak data entries

        Param data: a list of data points to parse through and find the index of the most recent data point
    """
    index = None
    for i in range(len(data)-1,0, -1): #count backwards through the list, starting at most recent append.
        if data[i] != None: #found most recent append containing data (not NoneType)
            debug("index found...data: %s" % (data[i]))
            return i #index for most recent append to list
        #END IF
    #END FOR
    return index #index will be none if this runs, signifying that no data point existed in the list
#end search_for_nums


def read_from_thingspeak(URL, KEY, FIELD, name):
    """A function that searches for the most recent entry in the desired field of a desired thingspeak channel

        Param URL: a string URL read request from a ThingSpeak channel
        Param KEY: a string read API Key for the ThingSpeak channel
        Param FIELD: a string containing the field to be parsing through
        Param name: a string name of the data being search for.  used it debug statements.
    """
    results = 1 #the exponent of base 2 number of results to request
    prev_len_data = 0 #the length of the list of data points collected on the previous loop search

    while (1):
        HEADER='&results=%d' % (2**results)
        NEW_URL=URL+KEY+HEADER

        try:
            get_data=requests.get(NEW_URL).json()

            data = []
            for x in get_data['feeds']:
                debug(x[FIELD])
                data.append(x[FIELD]) #get lightstatus
            #END for

            debug("length of data = %d " % (len(data)))

            index = search_for_nums(data) #searching for most recent lightstatus input

            if index != None: #found most recent data
                debug("data point found...%s: %s " % (name, data[index]))
                return int(data[index])

            else:
                debug("missing data point")
                results += 1

                if prev_len_data == len(data): #if the list of data previously collected is the same as the current
                    debug("No data points currently exist") #all current available data has been exhausted.  Move on
                    return
                else:
                    prev_len_data = len(data) #there are more points available.  try again.
                #END if
            #END if
        except:
            debug("Error reading %s from ThingSpeak" % (name))
        #END try-except
    #END WHILE

#END read_from Thingspeak


def read_light_status_from_thingspeak():
    """A function that searches for the most recent entry in the light status field of a thingspeak channel"""
    URL='https://api.thingspeak.com/channels/1153034/feeds.json?api_key='
    KEY='GAMCQ1Z7S3JQJH3I'

    return read_from_thingspeak(URL, KEY, "field1", "light_status")
#END read_light_status_from_thingspeak


def read_blinds_status_from_thingspeak():
    """A function that searches for the most recent entry in the blinds status field of a thingspeak channel"""
    URL='https://api.thingspeak.com/channels/1153034/feeds.json?api_key='
    KEY='GAMCQ1Z7S3JQJH3I'

    return read_from_thingspeak(URL, KEY, "field2", "blinds_status")
#END read_blinds_status_from_thingspeak


def motor_up(time, lock):
    """A function that causes the motors to roll up

        Param time: the time to have the motors active
        Param lock: a locking mutex
    """
    lock.acquire() #lock process
    debug("Motor up")
    GPIO.output(17, GPIO.LOW) #set input 1 to logic low
    GPIO.output(27, GPIO.HIGH) #set input 2 to logic high

    sleep(time)

    motor_stop()
    lock.release() #unlock process
#END counter_clockwise


def motor_down(time, lock):
    """A function that causes the motors to roll down

        Param time: the time to have the motors active
        Param lock: a locking mutex
    """
    lock.acquire() #lock process
    debug("Motor down")
    GPIO.output(17, GPIO.HIGH) #set input 1 to logic high
    GPIO.output(27, GPIO.LOW) #set input 2 to logic low

    sleep(time)

    motor_stop()
    lock.release() #unlock process
#END clockwise


def motor_stop():
    """A function that stops the motor rotation"""
    #reset values to logic low
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
#END motor_stop


def LED_init():
    """A function that initializes the LED GPIO pin"""
    GPIO.setup(18, GPIO.OUT) #LED enable
#END LED_init


def motor_init():
    """A function that initializes the motor GPIO pins"""
    GPIO.setup(4, GPIO.OUT) #Motor enable
    GPIO.setup(17, GPIO.OUT) #H-Bridge input 1
    GPIO.setup(27, GPIO.OUT) #H-Bridge input 2
#END motor_init


def camera_init(width, height):
    """A function that initializes a global camera object

        Param width: the desired pixel width of the image
        Param height: the desired pixel height of the image
    """
    global camera
    camera = PiCamera()
    camera.resolution = (width, height)
#END camera_init


def peripherals_init():
    """A function that calls the initlization functions of the peripheral devices"""
    LED_init()
    motor_init()
    camera_init(64, 64) #make resolution as small as possible to increase calculation efficiency
#END peripherals_init


def LED_on():
    """A fucntion that turns the LED on"""
    debug("LED on")
    GPIO.output(18, GPIO.HIGH) #Turn on LED
#END LED_on


def LED_off():
    """A fucntion that turns the LED off"""
    debug("LED off")
    GPIO.output(18, GPIO.LOW) #Turn off LED
#END LED_off


def check_light (light_status):
    """A function that checks if there has been a change in the light_status variable, and if so calls the appropriate functions to perform the desired action

        Param light_status: the desired status of the light
    """
    if not (check_light.prev_light_status == light_status): #if the value has changed
        check_light.prev_light_status = light_status #update the value for record
        if (light_status == 1): #turn on light
            LED_on()
        elif (light_status == 0): #turn off light
            LED_off()
        #END if
    #END if
#END check_light


def check_blinds(blinds_status, motor_lock):
    """A fucntion that checks if there has been a change in the blinds_status variable, and if so creates a concurrent thread to perform the desired action

        Param blinds_status: the desired status of the blinds
        Param motor_lock: a lock object for the motor (python equivalent of a mutex)
    """
    time = 10 #time to run the motor for
    if not (check_blinds.prev_blinds_status == blinds_status): #if the value has changed
        check_blinds.prev_blinds_status = blinds_status #update the value for record
        if (blinds_status == 1): #open blinds
            debug("Calling motor_up")
            up = Thread(target=motor_up, args = (time, motor_lock), daemon = False) #create thread object
            up.start() #start thread
        elif (blinds_status == 0): #close blinds
            debug("Calling motor_down")
            down = Thread(target=motor_down, args = (time, motor_lock), daemon = False) #create thread object
            down.start() #start thread
        #END if
    #END if
#END check_blinds


#main---------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        testing() #calls initial test cases

        #setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        peripherals_init() #initliaze all peripheral devices

        #these variables will only every be access in those functions, so do not need to be global, but must also keep record so cannot be local.
        #this is the python equivalent of a static variable. they are bound to their functions.
        check_light.prev_light_status = 0
        check_blinds.prev_blinds_status = 0
        
        motor_lock = Lock()

        while True:
            luma = current_average_luma()

            debug("the average luma of the image is: %f" %(luma)) #print light value

            write_to_thingspeak(luma)
            light_status = read_light_status_from_thingspeak()
            blinds_status = read_blinds_status_from_thingspeak()

            check_light(light_status)
            check_blinds(blinds_status, motor_lock)

            sleep(1.5)
        #END WHILE
    except:
        debug("Catastophic system error. Shutting down")
        camera.close()
        GPIO.cleanup()
    #END try-except
#END main
