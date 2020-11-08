import urllib.request
import requests
from time import sleep
import json

def search_for_nums(data):
    index1 = None 
    index2 = None
    
    for i in range(len(data)-1,0, -1): #count backwards through the loop
        if data[i] != None: #if a data point exists
            if index1 == None: #if an index is found, and index 1 has not yet been found
                print("index 1 found...data1: %s" % (data[i]))
                index1 = i
                
            elif index2 == None: #if an index is found, and index 1 has been found
                print("index 2 found...data2: %s" % (data[i]))
                index2 = i
                return (index1, index2)
            #END IF
        #END IF
    #END FOR
    return (index2, index1) #since we are counting backwards, we must invert the order so that it interprets it correctly 
#end search_for_nums
            
def read_from_thingspeak():
    results = 1
    URL='https://api.thingspeak.com/channels/1152832/fields/1.json?api_key='
    KEY='4DDGV289MS3GJCBY'
    
    while(1): #infinite loop until the data points are found
        HEADER='&results=%d' % (2**results) #increase by factor of 2
        NEW_URL=URL+KEY+HEADER
        get_data=requests.get(NEW_URL).json()
        
        data = []
        for x in get_data['feeds']:
            print(x['field1'])
            data.append(x['field1'])
        #END FOR
            
        if len(data) < 2: #if there are not enough data points available at this point in time, set both to 0
            print("not enough data points exist yet.  defaults to 0")
            return (0, 0)
        #END IF
        
        (index1, index2) = search_for_nums(data)
        
        if index1 != None and index2 != None: #both data points included in request
            print("both data points included in request...data1: %s data2: %s" % (data[index1], data[index2]))
            return (float(data[index1]), float(data[index2]))
        
        else: #missing a data point
            print("missing one or more data points")
            results += 1
        #END IF
    #END WHILE
#END read_from_thingspeak

def check_if_crossed(data1, data2, threshold):
    print ("checking if data crossed threshold")
    
    if (data1 < threshold and data2 > threshold): #if data crossed over threshold
        print("data went over threshold")
        write_to_thingspeak(0, 0) #turn off light, close blinds
        
    elif (data1 > threshold and data2 < threshold): #if data crossed under threshold
        print("data went under threshold")
        write_to_thingspeak(1, 1) #turn on light, open blinds
        
    else:
        print("data did not cross threshold")
    #END IF
#END check_if_crossed
        
def write_to_thingspeak(lighton, blindson):
    print("writing to thingspeak...lighton: %f blindson: %f" % (lighton, blindson))
    
    URl='https://api.thingspeak.com/update?api_key='
    KEY='VDHAE4N7ZXBU5P5K'
    HEADER='&field2={}&field3={}'.format(lighton, blindson)
    NEW_URL=URl+KEY+HEADER
    urllib.request.urlopen(NEW_URL)
    
    print("successfully written to thingspeak")
#END write_to_thingspeak
    
#MAIN
threshold = 100 #NOTE: this is a default value.  This value can be changed by the user

#these 3 will be changed through the GUI by the user
manual_override = False 
manual_light_status = 1
manual_blinds_status = 1

while(1):
    if not(manual_override): #if the user has not selected manual override
        (data1, data2) = read_from_thingspeak()
        check_if_crossed(data1, data2, threshold)

    else: #if the user has selected manual override
        write_to_thingspeak(manual_light_status, manual_blinds_status)
    #END IF
        
    sleep(4)
#END WHILE
