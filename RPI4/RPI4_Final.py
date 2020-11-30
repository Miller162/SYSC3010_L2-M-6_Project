"""Rpaspberry Pi 4 script

This script reads lumanence values from a ThingSpeak channel and then determines if the values have crossed a user-specified, or default threshold
If it has crossed the threshold it will write values to the ThingSpeak indicating another system to open or close blinds, and turn on or off a light based upon the direction in which the light data crossed the threshold.

IMPORTANT NOTE: in order to calibrate the system, the user must ensure that data crosses the system towards the beginning of its function.
If this is not done, the system will not behave properly until the light values naturally cross the threshold.

This file can be imported as a module with the following functions:

    *debug - A function that allows for easy printing of statements for debugging
    *search_for_nums - A function that searched for and returns the 2 most recent values in a list with possible Nonetypes
    *read_from_thingspeak - A function that retrieves data from a ThingSpeak channel and reads for the 2 most recent values in field1
    *check_if_crossed - A function that checks if the 2 data points have crossed the threshold
    *write_to_thingspeak - A function that writes lighton and blindson to field 2 and 3, respectively, to a ThingSpeak channel
    *main - A function that calls all the other functions in the file
"""

def debug(phrase):
    """A function that allows for easy printing of statements for debugging

        Param phrase: the phrased to be printed during debug
    """
    DEBUG = True #turn to True to get debugging print statements

    if (DEBUG): #if debug is active
        print(phrase)
    #END if
#END debug

#Imports------------------------------------------------------------------------
try:
    import urllib.request
except ImportError:
    debug("URLLIB module could not be imported")
else:
    debug("URLLIB module imported successfully")
#END try-except

try:
    import requests
except ImportError:
    debug("Requests module could not be imported")
else:
    debug("Requsts module imported successfully")
#END try-except

try:
    from time import sleep
except ImportError:
    debug("Time module could not be imported")
else:
    debug("Time module imported successfully")
#END try-except

try:
    import json
except ImportError:
    debug("JSON module could not be imported")
else:
    debug("JSON module imported successfully")
#END try-except


#Fucntions----------------------------------------------------------------------
def search_for_nums(data):
    """A function that searched for and returns the 2 most recent values in a list with possible Nonetypes

    If no values are found it will return 2 Nones.  If 1 value is found it will return 1 None and 1 value

        Param data: a list of containing None types and numbers
    """
    index1 = None
    index2 = None

    for i in range(len(data)-1,0, -1): #count backwards through the loop
        if data[i] != None: #if a data point exists
            if index1 == None: #if an index is found, and index 1 has not yet been found
                debug("Index 1 found...data1: %s" % (data[i]))
                index1 = i

            elif index2 == None: #if an index is found, and index 1 has been found
                debug("Index 2 found...data2: %s" % (data[i]))
                index2 = i
                return (index2, index1) #since data is found bakcwords, we should return them in opposite order of found
            #END IF
        #END IF
    #END FOR
    debug("2 indexes not found.  Return values will contain 1 or 2 None values")
    return (index2, index1) #since data is found bakcwords, we should return them in opposite order of found
#end search_for_nums


def read_from_thingspeak():
    """A function that retrieves data from a ThingSpeak channel and reads for the 2 most recent values in field1"""
    results = 1
    URL='https://api.thingspeak.com/channels/1152832/fields/1.json?api_key='
    KEY='4DDGV289MS3GJCBY'

    try:
        while(1): #infinite loop until the data points are found
            HEADER='&results=%d' % (2**results) #increase by factor of 2
            NEW_URL=URL+KEY+HEADER
            get_data=requests.get(NEW_URL).json() #prompt for data

            #collect all data in field1
            data = []
            for x in get_data['feeds']:
                debug(x['field1'])
                data.append(x['field1'])
            #END FOR

            if len(data) < 2: #if there are not enough data points available at this point in time, set both to 0
                debug("Not enough data points exist yet. Defaults return values to 0")
                return (0, 0)
            #END IF

            (index1, index2) = search_for_nums(data) #find indexes of most recent data points

            if index1 != None and index2 != None: #both data points included in request
                debug("Both data points included in request...data1: %s data2: %s" % (data[index1], data[index2]))
                return (float(data[index1]), float(data[index2]))

            else: #missing a data point
                debug("Missing one or more data points")
                results += 1
            #END IF
        #END WHILE
    except IndexError:
        debug("Attempting to access index out of range. Defaults return values to 0")
        return (0, 0)
    except:
        debug("Error reading from ThingSpeak. Defaults return values to 0")
        return (0, 0)
    #END try-except
#END read_from_thingspeak


def check_if_crossed(data1, data2, threshold):
    """A function that checks if the 2 data points have crossed the threshold

        Param data1: The first data point
        Param data2: The second data point
        Param threshold: the specified threshold
    """
    debug("Checking if data crossed threshold")

    if (data1 < threshold and data2 > threshold): #if data crossed over threshold
        debug("Data went over threshold. Turning light off. Closing blinds")
        write_to_thingspeak(0, 0) #turn off light, close blinds

    elif (data1 > threshold and data2 < threshold): #if data crossed under threshold
        debug("Data went under threshold. Turning on light. Opening blinds")
        write_to_thingspeak(1, 1) #turn on light, open blinds

    else:
        debug("data did not cross threshold")
    #END IF
#END check_if_crossed


def write_to_thingspeak(lighton, blindson):
    """A function that writes lighton and blindson to field 2 and 3, respectively, to a ThingSpeak channel

        Param lighton: A variable (either 0 or 1) that specifies the desired status of the light
        Param blindson: A variable (either 0 or 1) that specifies the desired status of the blinds
    """
    debug("writing to ThingSpeak...lighton: %f blindson: %f" % (lighton, blindson))

    URl='https://api.thingspeak.com/update?api_key='
    KEY='IP2POKYXDA3HXMGR'
    HEADER='&field1={}&field2={}'.format(lighton, blindson)
    NEW_URL=URl+KEY+HEADER

    try:
        urllib.request.urlopen(NEW_URL)
    except:
        debug("Error writing to ThingSpeak")
    else:
        debug("successfully written to ThingSpeak")
    #END try-except
#END write_to_thingspeak


def main(threshold, manual_override, manual_light_status, manual_blinds_status):
    """A function that calls all the other functions in the file.

        Param threshold: A variable that specifies the desired light threshold for light and blind automation
        Param manual_override: A boolean value that specifies whether the user wishes to take manual control of the light and blinds, rather than automated.
        Param manual_light_status: A variable (either 0 or 1) that specifies the users desired status of the light
        Param manual_blinds_status: A variable (either 0 or 1) that specifies the users desired status of the blinds
    """
    if not(manual_override): #if the user has not selected manual override
        (data1, data2) = read_from_thingspeak()
        check_if_crossed(data1, data2, threshold)

    else: #if the user has selected manual override
        write_to_thingspeak(manual_light_status, manual_blinds_status)
    #END IF
#END main
