import PIL
import urllib.request
import requests
from PIL import Image
from picamera import PiCamera
from time import sleep
import json
    
def current_average_luma(camera):
    camera.capture('/home/pi/Desktop/image1.jpg')#camera take picture
    img = Image.open("/home/pi/Desktop/image1.jpg") #opens image
    
    luma=0 #sum of the luma of each pixels
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
    URl='https://api.thingspeak.com/update?api_key='
    KEY='VDHAE4N7ZXBU5P5K'
    HEADER='&field1={}'.format(luma)
    NEW_URL=URl+KEY+HEADER
    urllib.request.urlopen(NEW_URL)
#END sent_to_thingspeak
    
def search_for_nums(data):
    
    index = None
    for i in range(len(data)-1,0, -1): #count backwards through the loop
        if data[i] != None: #found most recent input
            print("index found...data: %s" % (data[i]))
            return i
        #END IF
    #END FOR
    return index #since we are counting backwards, we must invert the order so that it interprets it correctly 
#end search_for_nums

def read_light_status_from_thingspeak():
    results = 1
    URL='https://api.thingspeak.com/channels/1152832/feeds.json?api_key='
    KEY='4DDGV289MS3GJCBY'
    
    while (1):
        HEADER='&results=%d' % (2**results)
        NEW_URL=URL+KEY+HEADER
        get_data=requests.get(NEW_URL).json()
        
        data = []
        for x in get_data['feeds']:
            print(x['field2'])
            data.append(x['field2']) #get lightstatus
            
        if len(data) == 0: #if there are no points available
            print("not enough lightstatus data points at this time")
            return
        #END IF
            
        index = search_for_nums(data) #searching for most recent lightstatus input
        
        if index != None: #found most recent data
            print("data point found...lighstatus: %s " % (data[index]))
            return int(data[index])
        else:
            print("missing data point")
            results += 1
    #END WHILE
#END read_light_status_from_thingspeak

def read_blinds_status_from_thingspeak():
    results = 1
    URL='https://api.thingspeak.com/channels/1152832/feeds.json?api_key='
    KEY='4DDGV289MS3GJCBY'
    
    while (1):
        HEADER='&results=%d' % (2**results)
        NEW_URL=URL+KEY+HEADER
        get_data=requests.get(NEW_URL).json()
        
        data = []
        for x in get_data['feeds']:
            print(x['field3'])
            data.append(x['field3']) #get lightstatus
            
        if len(data) == 0: #if there are no points available
            print("not enough blindsstatus data points at this time")
            return
        #END IF
            
        index = search_for_nums(data) #searching for most recent lightstatus input
        
        if index != None: #found most recent data
            print("data point found...blindsstatus: %s " % (data[index]))
            return int(data[index])
        else:
            print("missing data point")
            results += 1
    #END WHILE
#END read_blinds_status_from_thingspeak
            
#MAIN
camera = PiCamera() #setting the camera object
camera.resolution = (64, 64) #set resolution (keep as small as possible to avoid lengthy calculations

while (1):
    luma = current_average_luma(camera)
    print("the average luma of the image is: ", luma) #print light value
    write_to_thingspeak(luma)
    light_status = read_light_status_from_thingspeak()
    blinds_status = read_blinds_status_from_thingspeak()
    
    sleep(4)
#END WHILE