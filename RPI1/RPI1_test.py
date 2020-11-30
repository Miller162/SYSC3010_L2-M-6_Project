""""Raspberry Pi 1 test script

This script will test all the device tasks, including communicating with ThingSpeak, and all peripheral devices.
The overall purpose of this script is to calculate the lumenance of the area the Raspberry Pi is located in, send that data to a Thingspeak channel,
then read values from a ThingSpeak channel and turn on a light or open blinds depending on those values.

This file can be imported as a module with the following functions:

    *testing - this function runs test cases for the peripherals that have been imported from external files
    *current_average_luma - this function captures an image via the Pi Camera and calculates the average lumenance of that image
    *write_to_thingspeak - this function writes the average lumenance data from thingspeak
    *search_for_nums - this function searches for the most recent input from a list of thingspeak data entries
    *read_light_status_from_thingspeak - this function searches for the most recent entry in the light status field of a thingspeak channel
    *read_blinds_status_from_thingspeak - this function searches for the most recent entry in the blinds status field of a thingspeak channel
"""

import urllib.request
import requests
from PIL import Image
from picamera import PiCamera
from time import sleep
import json
import RPI1_LED_test
import RPI1_PiCam_test
import RPI1_Motor_test

def testing():
    """This function runs test cases for the peripherals that have been imported from external files"""
    RPI1_LED_test.LED_test()
    sleep(1)
    RPI1_PiCam_test.PiCam_test()
    sleep(1)
    RPI1_Motor_test.Motor_test()
    sleep(1)

    GPIO.cleanup()
#END testing

def current_average_luma(camera):
    """This function captures an image via the Pi Camera and calculates the average lumenance of that image"""
    camera.capture('/home/pi/Desktop/image1.jpg')#camera take picture
    img = Image.open("/home/pi/Desktop/image1.jpg") #opens image

    luma=0 #sum of the lumenance of each pixels
    pixels = img.width*img.height #number of pixels

    for x in range(img.width):
        for y in range(img.height):
            (r, g, b) = img.getpixel((x,y))#get colour touple
            luma += (0.2126*r + 0.7152*g + 0.0722*b) #calculate luma of RGB data, then add to total
        #END for
    #END for

    img.close()#ensure to properly close the image
    return luma/pixels #return average of all pixels
#END average_luma

def write_to_thingspeak(luma):
    """This function writes the average lumenance data from thingspeak"""
    URl='https://api.thingspeak.com/update?api_key='
    KEY='VDHAE4N7ZXBU5P5K'
    HEADER='&field1={}'.format(luma)
    NEW_URL=URl+KEY+HEADER

    try:
        urllib.request.urlopen(NEW_URL)
    except:
        print ("Error writing to ThingSpeak")
    else:
        print ("Successfully written to ThingSpeak")
    #END try-except
#END sent_to_thingspeak

def search_for_nums(data):
    """This function searches for the most recent input from a list of thingspeak data entries"""
    index = None
    for i in range(len(data)-1,0, -1): #count backwards through the loop, starting at most recent append
        if data[i] != None: #found most recent input
            print("index found...data: %s" % (data[i]))
            return i
        #END IF
    #END FOR
    return index
#end search_for_nums

def read_light_status_from_thingspeak():
    """This function searches for the most recent entry in the light status field of a thingspeak channel"""
    results = 1
    URL='https://api.thingspeak.com/channels/1152832/feeds.json?api_key='
    KEY='4DDGV289MS3GJCBY'
    prev_len_data = 0 #the length of the list of data points collected on the previous loop search

    while (1):
        HEADER='&results=%d' % (2**results)
        NEW_URL=URL+KEY+HEADER

        try:
            get_data=requests.get(NEW_URL).json()

            data = []
            for x in get_data['feeds']:
                print(x['field2'])
                data.append(x['field2']) #get lightstatus
            #END for

            print ("length of data = %d " % (len(data)))

            index = search_for_nums(data) #searching for most recent lightstatus input

            if index != None: #found most recent data
                print("data point found...lighstatus: %s " % (data[index]))
                return int(data[index])
            else:
                print("missing data point")
                results += 1

                if prev_len_data == len(data): #if the list of data previously collected is the same as the current
                    print ("No data points currently exist") #all current available data has been exhausted.  Move on
                    return
                else:
                    prev_len_data = len(data) #there are more points available.  try again.
                #END if
            #END if
        except:
            print ("Error reading light_status from ThingSpeak")
        #END try-except
    #END WHILE
#END read_light_status_from_thingspeak

def read_blinds_status_from_thingspeak():
    """This function searches for the most recent entry in the blinds status field of a thingspeak channel"""
    results = 1
    URL='https://api.thingspeak.com/channels/1152832/feeds.json?api_key='
    KEY='4DDGV289MS3GJCBY'
    prev_len_data = 0 #the length of the list of data points collected on the previous loop search

    while (1):
        HEADER='&results=%d' % (2**results)
        NEW_URL=URL+KEY+HEADER

        try:
            get_data=requests.get(NEW_URL).json()

            data = []
            for x in get_data['feeds']:
                print(x['field3'])
                data.append(x['field3']) #get lightstatus
            #End for

            index = search_for_nums(data) #searching for most recent lightstatus input

            if index != None: #found most recent data
                print("data point found...blindsstatus: %s " % (data[index]))
                return int(data[index])
            else:
                print("missing data point")
                results += 1

                if prev_len_data == len(data): #if the list of data previously collected is the same as the current
                    print ("No data points currently exist") #all current available data has been exhausted.  Move on
                    return
                else:
                    prev_len_data = len(data) #there are more points available.  try again.
                #END if
            #END if
        except:
            print ("Error reading blinds_status from ThingSpeak")
        #END try-except
    #END WHILE
#END read_blinds_status_from_thingspeak

#MAIN
testing() #calls initial test cases

camera = PiCamera() #setting the camera object
camera.resolution = (64, 64) #set resolution (keep as small as possible to avoid lengthy calculations

while(1):
    luma = current_average_luma(camera)
    print("the average luma of the image is: ", luma) #print light value
    write_to_thingspeak(luma)
    light_status = read_light_status_from_thingspeak()
    blinds_status = read_blinds_status_from_thingspeak()

    sleep(4)
#END WHILE

camera.close()
