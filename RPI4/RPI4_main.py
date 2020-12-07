"""
This code reads data from all the ThingSpeak channels and sorts
it into lists, it then placed the data in a database and calls
other programs for the GUI and the LED display on the SenseHat.
Additionally, it sends out email notifications.
"""
try:
    import urllib.request
except:
    print("could not import urllib.request")
try:
    import requests
except:
    print("could not import requests")
try:
    import sqlite3
except:
    print("could not import sqlite3")
try:
    from threading import Thread
except:
    print("could not import threading")
try:
    import RPI4_Final
except:
    print("could not import RPI4_Final")
try:
    import RPI4_GUI3
except:
    print("could not import RPI4_GUI3")
try:   
    import RPI4_Temp
except:
    print("could not import RPI4_Temp")
try:
    import emailAlert
except:
    print("could not import emailAlert")
try:
    from time import sleep
except:
    print("could not import time")

#Group members:
#A Miller, RPi1
#B Gurjit, RPi2
#C Eric,   RPi4
#D Akkash, RPi3

#DEBUG: set to True to enable debug functionality
debugFlag = False

#stops multiple emails from being sent
#flag for temp warning
global emailFlagValue1
emailFlagValue1 = 0

#flag for seismic warning
global emailFlagValue2
emailFlagValue2 = 0 

#Channel names
nameA1 = "Channel L2-M-6A1"
nameB1 = "Channel L2-M-6B1"
nameC1 = "Channel L2-M-6C1"
nameD2 = "Channel L2-M-6D2"

#Write API keys
writeKeyA1 = "VDHAE4N7ZXBU5P5K"
writeKeyB1 = "JOHC5J4TZM2L3PPF"
writeKeyC1 = "IP2POKYXDA3HXMGR"
writeKeyD2 = "0QXHFFZLS3MB2Z0A"

#Read API keys
readKeyA1 = "4DDGV289MS3GJCBY"
readKeyB1 = "81HMLN4DJFA037FV"
readKeyC1 = "GAMCQ1Z7S3JQJH3I"
readKeyD2 = "HHS2A1XQ1MN2HMAP"

#channel IDs
idA1 = "1152832"
idB1 = "1165995"
idC1 = "1153034"
idD2 = "1158485"

#Write URLs
writeUrl = "https://api.thingspeak.com/update?api_key="

#read URLs
readUrl = "https://api.thingspeak.com/channels/{}/feeds.json?api_key="
readUrlA1 = readUrl.format(idA1)
readUrlB1 = readUrl.format(idB1)
readUrlC1 = readUrl.format(idC1)
readUrlD2 = readUrl.format(idD2)

#database tables
tableA1 = "RPI1_log"
tableB1 = "RPI2_log"
tableC1 = "RPI4_log"
tableD2 = "RPI3_log"

#database table sizes (number of columns)
sizeA1 = 3
sizeB1 = 6
sizeC1 = 4
sizeD2 = 4

#database table arguments (used to simplify insertions later; make the code more modular)
argA1 = "(dateTime, tsid, lightLevel) VALUES(?, ?, ?)"
argB1 = "(dateTime, tsid, temperature, pressure, humidity, gyroscope) VALUES(?, ?, ?, ?, ?, ?)"
argC1 = "(dateTime, tsid, lightStatus, blindStatus) VALUES(?, ?, ?, ?)"
argD2 = "(dateTime, tsid, windSpeed, windDirection) VALUES(?, ?, ?, ?)"

#Database connection setup
try:
    dbconnect = sqlite3.connect("database.db")
    dbconnect.row_factory = sqlite3.Row
    cursor = dbconnect.cursor()
except:
    print("failure to connect to database file")

#Database table setup
try:
    cursor.execute("CREATE TABLE IF NOT EXISTS  RPI1_log (dateTime TEXT, tsid NUMERIC, lightLevel NUMERIC)")
    cursor.execute("CREATE TABLE IF NOT EXISTS  RPI2_log (dateTime TEXT, tsid NUMERIC, temperature NUMERIC, pressure NUMERIC, humidity NUMERIC, gyroscope TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS  RPI3_log (dateTime TEXT, tsid NUMERIC, windSpeed NUMERIC, windDirection TEXT)") 
    cursor.execute("CREATE TABLE IF NOT EXISTS  RPI4_log (dateTime TEXT, tsid NUMERIC, lightStatus BOOLEAN, blindStatus BOOLEAN)")
    dbconnect.commit()
except:
    print("failure to establish database tables")

def checkHighestEntry(channel):
    cursor.execute('SELECT * FROM %s' %channel.table)
    highestEntry = 0
    for row in cursor:
        if int(row['tsid']) > highestEntry:
            highestEntry = row['tsid']
    channel.dbHighestEntry = highestEntry

#Insert data into databasr tables
def insertData(dataList, channel, tableSize):
    #print("DEBUG: tableSize: ", tableSize)
    if tableSize == 3:
        cursor.execute("INSERT INTO %s %s" %(channel.table, channel.arguments), (dataList[0], dataList[1], dataList[2]))    
    if tableSize == 4:
        cursor.execute("INSERT INTO %s %s" %(channel.table, channel.arguments), (dataList[0], dataList[1], dataList[2], dataList[3]))    
    if tableSize == 5:
        cursor.execute("INSERT INTO %s %s" %(channel.table, channel.arguments), (dataList[0], dataList[1], dataList[2], dataList[3], dataList[4]))
    if tableSize == 6:
        cursor.execute("INSERT INTO %s %s" %(channel.table, channel.arguments), (dataList[0], dataList[1], dataList[2], dataList[3], dataList[4], dataList[5]))
    dbconnect.commit()
    
def writeToDatabase(channel):
    i = channel.dbHighestEntry
    while i < channel.lastEntryId:
        insertData(Channel.createEntryList(channel, i), channel, channel.tableSize)
        i += 1

#close the connection when safe to do so
def dbClose():
    if dbconnect.in_transaction == False:
        cursor.close()
        dbconnect.close()

#update the database corresponding to a channel
def update(channel):
    checkHighestEntry(channel)
    if channel.lastEntryId is None:
        print("The ThingSpeak channel (%s) is cleared, nothing to write to database (table: %s)" %(channel.name, channel.table))
    elif channel.dbHighestEntry > channel.lastEntryId:
        print("The local database file (table: %s) is out of synch with ThingSpeak %s; the ThingSpeak channel was probably cleared without also resetting the database" %(channel.table, channel.name))
        print("\n Recommendation: delete the database file; a new one will be created on the next execution")
    else:
        checkHighestEntry(channel)
        print("Last Entry before updating database (%s, table: %s): %s" %(channel.name, channel.table, channel.dbHighestEntry))
        writeToDatabase(channel)
        checkHighestEntry(channel)
        print("Last Entry after updating database (%s, table: %s): %s" %(channel.name, channel.table, channel.dbHighestEntry))    

#define static channel methods
def checkChannelInput(prompt):
    while True:
        channelSelect = input(prompt)
        if channelSelect == 'A':
            print("channel A selected")
            return channelA1
        elif channelSelect == 'B':
            print("channel B selected")
            return channelB1
        elif channelSelect == 'C':
            print("channel C selected")
            return channelC1
        elif channelSelect == 'D':
            print("channel D selected")
            return channelD2
        else:
            print("invalid response, try again")

#used to navigate the shell
def checkEntryInput(prompt, usrChannel):
    good = False
    while True:
        entrySelect = input(prompt)
        try:
            entrySelect = int(entrySelect)
            good = True
        except:
            print("not an int")
            good = False
        if good:
            print("Entry " + str(entrySelect) + ": ", Channel.createEntryList(usrChannel, entrySelect-1))
            good = False

#used to make sending email notifications easier
def email_update(email_obj, recipient, channel):
    global emailFlagValue1
    global emailFlagValue2
    temp_str =  ""
    gyro_str = ""
    highestRecord1 = 0
    highestRecord2 = 0
    #details for temperature
    subject_temp = "WARNING: High Temperature"
    message_temp = "The current temperature in the house exceeds the set threshold. User action is required."   
    #details for seismic activity
    subject_gyro = "WARNING: Seismic Activity"
    message_gyro = "Seismic activity has been detected. User action is required."      
    cursor.execute("SELECT * FROM %s ORDER BY tsid DESC LIMIT 1" %channel.table)
    for row in cursor:
        temp_str = row["temperature"]
        highestRecord1 = int(row["tsid"])
    print("Current temp: ", temp_str)
    try:
        temp = int(temp_str)
    except:
        temp = 0
    if temp >= 30 and highestRecord1 > emailFlagValue1:
        emailFlagValue1 = highestRecord1
        email_obj.notifyUser(recipient, subject_temp, message_temp)
    cursor.execute("SELECT * FROM %s ORDER BY tsid DESC LIMIT 1" %channel.table)
    for row in cursor:
        gyro_str = row["gyroscope"]
        highestRecord2 = int(row["tsid"])
    print("Seismic activity: ", gyro_str)
    if gyro_str != "Undetected" and highestRecord2 > emailFlagValue2:
        emailFlagValue2 = highestRecord2
        email_obj.notifyUser(recipient, subject_gyro, message_gyro)    
            
#DEBUG testing method
def debug(channel):
    print("Reading ThingSpeak %s" %channel.name)
    print("read URL: ", channel.readUrl)
    print("write URL: ", channel.writeUrl)
    print("Last entry ID: ", channel.lastEntryId)
    
    print("field1List: ", channel.field1List)
    print("field2List: ", channel.field2List)
    print("field3List: ", channel.field3List)
    print("field4List: ", channel.field4List)
    print("field5List: ", channel.field5List)
    print("field6List: ", channel.field6List)
    print("field7List: ", channel.field7List)
    print("field8List: ", channel.field8List)
    print("---------------------------------------------------")    

class Channel:
    #constructor method
    def __init__(self, readUrl, writeUrl, readApiKey, writeApiKey, cid, table, arguments, tableSize, name):
        self.readUrl = readUrl + readApiKey + "&results=8000"
        self.writeUrl = writeUrl + writeApiKey
        self.readApiKey = readApiKey
        self.writeApiKey = writeApiKey
        self.cid = cid
        self.table = table
        self.arguments = arguments
        self.tableSize = tableSize
        self.dbHighestEntry = 0
        self.name = name
        
        self.data = requests.get(self.readUrl).json()
        self.lastEntryId = self.data['channel']["last_entry_id"]
        self.feeds = self.data["feeds"]
        
        #initialize field lists
        self.field1List = []
        self.field2List = []
        self.field3List = []
        self.field4List = []
        self.field5List = []
        self.field6List = []
        self.field7List = []
        self.field8List = []    
    
    #read a channel once
    def readChannel(self, value, fieldString):
        try:
            for i in self.feeds:
                value.append(i[fieldString])
            return value
        except KeyError:
            if debugFlag:
                print(fieldString, "is empty")
        except:
            if debugFlag:
                print(fieldString, "is not empty but something went wrong")
    
    #populate field lists
    def createFieldLists(self):
        #update the last entry id
        self.data = requests.get(self.readUrl).json()
        self.lastEntryId = self.data['channel']["last_entry_id"]
        #clear field lists first
        self.field1List = []
        self.field2List = []
        self.field3List = []
        self.field4List = []
        self.field5List = []
        self.field6List = []
        self.field7List = []
        self.field8List = []     
        #then populate the field lists
        self.field1List = self.readChannel(self.field1List, "field1")
        self.field2List = self.readChannel(self.field2List, "field2")
        self.field3List = self.readChannel(self.field3List, "field3")
        self.field4List = self.readChannel(self.field4List, "field4")
        self.field5List = self.readChannel(self.field5List, "field5")
        self.field6List = self.readChannel(self.field6List, "field6")
        self.field7List = self.readChannel(self.field7List, "field7")
        self.field8List = self.readChannel(self.field8List, "field8")
    
    #create a list for a specified entry on ThingSpeak     
    def createEntryList(self, entryId):
        entryList = []
        entryList.append(self.data["feeds"][entryId]["created_at"])
        entryList.append(self.data["feeds"][entryId]["entry_id"])
        #print("Length of field1List is: ", len(self.field1List))
        #print("data: ", self.data["feeds"][entryId]["field1"])
        if self.field1List is not None:
            entryList.append(self.data["feeds"][entryId]["field1"])
        if self.field2List is not None:
            entryList.append(self.data["feeds"][entryId]["field2"])
        if self.field3List is not None:
            entryList.append(self.data["feeds"][entryId]["field3"])
        if self.field4List is not None:
            entryList.append(self.data["feeds"][entryId]["field4"])
        if self.field5List is not None:
            entryList.append(self.data["feeds"][entryId]["field5"])
        if self.field6List is not None:
            entryList.append(self.data["feeds"][entryId]["field6"])
        if self.field7List is not None:
            entryList.append(self.data["feeds"][entryId]["field7"])
        if self.field8List is not None:
            entryList.append(self.data["feeds"][entryId]["field8"])
        return entryList   

if __name__ == "__main__":
    
    #Set up channel objects
    channelA1 = Channel(readUrlA1, writeUrl, readKeyA1, writeKeyA1, idA1, tableA1, argA1, sizeA1, nameA1)
    Channel.createFieldLists(channelA1)

    channelB1 = Channel(readUrlB1, writeUrl, readKeyB1, writeKeyB1, idB1, tableB1, argB1, sizeB1, nameB1)
    Channel.createFieldLists(channelB1)
    
    channelC1 = Channel(readUrlC1, writeUrl, readKeyC1, writeKeyC1, idC1, tableC1, argC1, sizeC1, nameC1)
    Channel.createFieldLists(channelC1)
    
    channelD2 = Channel(readUrlD2, writeUrl, readKeyD2, writeKeyD2, idD2, tableD2, argD2, sizeD2, nameD2)
    Channel.createFieldLists(channelD2)
    
    #DEBUG testing
    if debugFlag:
        debug(channelA1)
        debug(channelB1)
        debug(channelC1)
        debug(channelD2)
        try:
            userChannel = checkChannelInput("Enter A, B, or D to select a channel: ")
        except:
            print("could not check input")
        
        checkEntryInput("Enter entry number to search for: ", userChannel)        
    
    try:          
        temp = Thread(target=RPI4_Temp.main, daemon = False)
        temp.start()
    except:
        print("sense hat error")
    
    #RPI4_Final.main(85, False, 1, 1) reminder for format when using RPI4_Final
    
    #setup email notifications
    email_obj = emailAlert.EmailNotification()
    recipient = RPI4_GUI3.get_email_input()
    print("recipient: ", recipient)
    
    while True:
        print("radio select value: ", RPI4_GUI3.radio_select_value())
        print("threshold value: ", RPI4_GUI3.get_input())
        print("manual light status: ", RPI4_GUI3.radio_preference_value_light())
        print("manual blind status: ", RPI4_GUI3.radio_preference_value_blind())
        
        RPI4_Final.main(RPI4_GUI3.get_input(), RPI4_GUI3.radio_select_value(), RPI4_GUI3.radio_preference_value_light(), RPI4_GUI3.radio_preference_value_blind())
            
        Channel.createFieldLists(channelA1)
        Channel.createFieldLists(channelB1)
        Channel.createFieldLists(channelC1)
        Channel.createFieldLists(channelD2)
        update(channelA1)
        update(channelB1)
        update(channelC1)
        update(channelD2)
        email_update(email_obj, recipient, channelB1)
        print("---------------------------------------------------")
        sleep(1)
    dbClose() #this line won't be reached but it's a good reminder to close files