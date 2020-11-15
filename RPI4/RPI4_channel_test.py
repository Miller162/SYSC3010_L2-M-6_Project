import urllib.request
import requests

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

class Channel:
    #constructor method
    def __init__(self, readUrl, writeUrl, readApiKey, writeApiKey, cid):
        self.readUrl = readUrl + readApiKey
        self.writeUrl = writeUrl + writeApiKey
        self.readApiKey = readApiKey
        self.writeApiKey = writeApiKey
        self.cid = cid
        
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
        
    #def createEntryIdList(self):
        #for i in self.feeds:
            #self.entryIdList.append(i["entry_id"])
        #self.higestEntryId = self.entryIdList[-1]
        ##print("idList",idList)        
    
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
        
    def createEntryList(self, entryId):
        entryList = []
        for i in self.data["feeds"][entryId]:
            entryList.append(i)
        return entryList

#Reading test
channelA1 = Channel(readUrlA1, writeUrl, readKeyA1, writeKeyA1, idA1)
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

channelB1 = Channel(readUrlB1, writeUrl, readKeyB1, writeKeyB1, idB1)
print("Reading ThingSpeak Channel L2-M-6B1")
print("read URL: ", channelB1.readUrl)
print("write URL: ", channelB1.writeUrl)
print("Last entry ID: ", channelB1.lastEntryId)
#Channel.createEntryList(channelB1, 1)
#print("Entry 1: ", Channel.createEntryList(channelB1, 1))

Channel.createFieldLists(channelB1)
print("field1List: ", channelB1.field1List)
print("field2List: ", channelB1.field2List)
print("field3List: ", channelB1.field3List)
print("field4List: ", channelB1.field4List)
print("field5List: ", channelB1.field5List)
print("field6List: ", channelB1.field6List)
print("field7List: ", channelB1.field7List)
print("field8List: ", channelB1.field8List)
print("---------------------------------------------------")

channelC1 = Channel(readUrlC1, writeUrl, readKeyC1, writeKeyC1, idC1)
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

channelD2 = Channel(readUrlD2, writeUrl, readKeyD2, writeKeyD2, idD2)
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
#field1List = []
#field1List = channelC1.readChannel(field1List)
#print("channel C1: ", field1List)