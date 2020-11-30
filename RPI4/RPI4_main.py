import urllib.request
import requests
import sqlite3

#Group members:
#A Miller, RPi1
#B Gurjit, RPi2
#C Eric,   RPi4
#D Akkash, RPi3

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
#writeUrlA1 = writeUrl + writeKeyA1
#writeUrlB1 = writeUrl + writeKeyB1
#writeUrlC1 = writeUrl + writeKeyC1
#writeUrlD2 = writeUrl + writeKeyD2

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
sizeA1 = 5
sizeB1 = 5
sizeC1 = 2
sizeD2 = 4

#database table arguments (used to simplify insertions later; make the code more modular)
argA1 = "(dateTime, tsid, lightLevel, lightStatus, blindStatus) VALUES(?, ?, ?, ?, ?)"
argB1 = "(dateTime, tsid, temperature, pressure, humidity) VALUES(?, ?, ?, ?, ?)" #gyroscope update: remove for now
argC1 = "(dateTime, cpuTemp) VALUES(?, ?)"
argD2 = "(dateTime, tsid, windSpeed, windDirection) VALUES(?, ?, ?, ?)" #updated: removed averageWindSpeed

#Database connection setup
try:
    dbconnect = sqlite3.connect("database.db")
    dbconnect.row_factory = sqlite3.Row
    cursor = dbconnect.cursor()
except:
    print("failure to connect to database file")

#Database table setup
try:
    cursor.execute("CREATE TABLE IF NOT EXISTS  RPI1_log (dateTime TEXT, tsid NUMERIC, lightLevel NUMERIC, lightStatus BOOLEAN, blindStatus BOOLEAN)")
    cursor.execute("CREATE TABLE IF NOT EXISTS  RPI2_log (dateTime TEXT, tsid NUMERIC, temperature NUMERIC, pressure NUMERIC, humidity NUMERIC)") #, gyroscope NUMERIC)")
    cursor.execute("CREATE TABLE IF NOT EXISTS  RPI3_log (dateTime TEXT, tsid NUMERIC, windSpeed NUMERIC, windDirection TEXT)") #, averageWindSpeed NUMERIC)") #IMPORTANT: confirm consistency across thingspeak
    cursor.execute("CREATE TABLE IF NOT EXISTS  RPI4_log (date TEXT, time TEXT, cpuTemp NUMERIC)")
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

class Channel:
    #constructor method
    def __init__(self, readUrl, writeUrl, readApiKey, writeApiKey, cid, table, arguments, tableSize):
        self.readUrl = readUrl + readApiKey
        self.writeUrl = writeUrl + writeApiKey
        self.readApiKey = readApiKey
        self.writeApiKey = writeApiKey
        self.cid = cid
        self.table = table
        self.arguments = arguments
        self.tableSize = tableSize
        self.dbHighestEntry = 0
        
        self.data = requests.get(self.readUrl).json()
        self.lastEntryId = self.data['channel']["last_entry_id"]
        #self.channelId = self.data['channel']['id']
        #print(self.cid)
        #print(self.channelId)
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
            print(fieldString, "is empty")
        except:
            print(fieldString, "is not empty but something went wrong")
    
    #populate field lists
    def createFieldLists(self):
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
    
    #Reading test, repetition will be resolved later via a function (hopefully)
    channelA1 = Channel(readUrlA1, writeUrl, readKeyA1, writeKeyA1, idA1, tableA1, argA1, sizeA1)
    print("Reading ThingSpeak Channel L2-M-6A1")
    print("read URL: ", channelA1.readUrl)
    print("write URL: ", channelA1.writeUrl)
    print("Last entry ID: ", channelA1.lastEntryId)
    
    Channel.createFieldLists(channelA1)
    print("field1List: ", channelA1.field1List)
    print("field2List: ", channelA1.field2List)
    print("field3List: ", channelA1.field3List)
    print("field4List: ", channelA1.field4List)
    print("field5List: ", channelA1.field5List)
    print("field6List: ", channelA1.field6List)
    print("field7List: ", channelA1.field7List)
    print("field8List: ", channelA1.field8List)
    print("---------------------------------------------------")
    
    channelB1 = Channel(readUrlB1, writeUrl, readKeyB1, writeKeyB1, idB1, tableB1, argB1, sizeB1)
    print("Reading ThingSpeak Channel L2-M-6B1")
    print("read URL: ", channelB1.readUrl)
    print("write URL: ", channelB1.writeUrl)
    print("Last entry ID: ", channelB1.lastEntryId)
    
    Channel.createFieldLists(channelB1)
    print("field1List: ", channelB1.field1List)
    print("field2List: ", channelB1.field2List)
    print("field3List: ", channelB1.field3List)
    print("field4List: ", channelB1.field4List)
    print("field5List: ", channelB1.field5List)
    print("field6List: ", channelB1.field6List)
    print("field7List: ", channelB1.field7List)
    print("field8List: ", channelB1.field8List)
    ##Create a list for one specific entry
    #print("Entry 1: ", Channel.createEntryList(channelB1, 1))
    print("---------------------------------------------------")
    
    channelC1 = Channel(readUrlC1, writeUrl, readKeyC1, writeKeyC1, idC1, tableC1, argC1, sizeC1)
    print("Reading ThingSpeak Channel L2-M-6C1")
    print("read URL: ", channelC1.readUrl)
    print("write URL: ", channelC1.writeUrl)
    print("Last entry ID: ", channelC1.lastEntryId)
    
    Channel.createFieldLists(channelC1)
    print("field1List: ", channelC1.field1List)
    print("field2List: ", channelC1.field2List)
    print("field3List: ", channelC1.field3List)
    print("field4List: ", channelC1.field4List)
    print("field5List: ", channelC1.field5List)
    print("field6List: ", channelC1.field6List)
    print("field7List: ", channelC1.field7List)
    print("field8List: ", channelC1.field8List)
    print("---------------------------------------------------")
    
    channelD2 = Channel(readUrlD2, writeUrl, readKeyD2, writeKeyD2, idD2, tableD2, argD2, sizeD2)
    print("Reading ThingSpeak Channel L2-M-6D2")
    print("read URL: ", channelD2.readUrl)
    print("write URL: ", channelD2.writeUrl)
    print("Last entry ID: ", channelD2.lastEntryId)
    
    Channel.createFieldLists(channelD2)
    print("field1List: ", channelD2.field1List)
    print("field2List: ", channelD2.field2List)
    print("field3List: ", channelD2.field3List)
    print("field4List: ", channelD2.field4List)
    print("field5List: ", channelD2.field5List)
    print("field6List: ", channelD2.field6List)
    print("field7List: ", channelD2.field7List)
    print("field8List: ", channelD2.field8List)
    print("---------------------------------------------------")

    #testList = ['2020-11-20T23:04:13Z', 1, '25.171300439452835', None, None]        
    #connection, cursor = dbConnect()
    #createTables(connection)
    #always check the databse entries first
    checkHighestEntry(channelA1)
    print("Last Entry before updating database (table: %s): %s" %(channelA1.table, channelA1.dbHighestEntry))
    writeToDatabase(channelA1)
    checkHighestEntry(channelA1)
    print("Last Entry after updating database (table: %s): %s" %(channelA1.table, channelA1.dbHighestEntry))
    
    checkHighestEntry(channelB1)
    print("Last Entry before updating database (table: %s): %s" %(channelB1.table, channelB1.dbHighestEntry))
    writeToDatabase(channelB1)
    checkHighestEntry(channelB1)
    print("Last Entry after updating database (table: %s): %s" %(channelB1.table, channelB1.dbHighestEntry))
    
    checkHighestEntry(channelD2)
    print("Last Entry before updating database (table: %s): %s" %(channelD2.table, channelD2.dbHighestEntry))
    writeToDatabase(channelD2)
    checkHighestEntry(channelD2)
    print("Last Entry after updating database (table: %s): %s" %(channelD2.table, channelD2.dbHighestEntry))     
    #writeToDatabase(channelB1)
    #writeToDatabase(channelA1, channelA1.table)
    #writeToDatabase(channelA1, channelA1.table)
    dbClose()
    
    
    try:
        userChannel = checkChannelInput("Enter A, B, C, or D to select a channel: ")
    except:
        print("could not check input")
    
    checkEntryInput("Enter entry number to search for: ", userChannel)
