import http.client
import urllib.parse
import urllib.request
import requests

bins = [[0,0,0],[0,0,0],[0,0,0]]
DEBUG = True


def readFromThingSpeak(bin_num):
  channelID = 1222563 + bin_num  
  URL="https://api.thingspeak.com/channels/" + str(channelID) + "/feeds.json?api_key="
  KEY='MG9FWWZOG8M0PCGK'
  HEADER='&results=1'
  NEW_URL=URL+KEY+HEADER

  get_data=requests.get(NEW_URL).json()

  feeds=get_data['feeds'][0]
  bins[bin_num][0] = int(feeds["field1"])
  bins[bin_num][1] = int(feeds["field2"])
  bins[bin_num][2] = int(feeds["field3"])


def writeToThingSpeak(tsKey, stationID):
    params = urllib.parse.urlencode({'field1': bins[stationID][0],'field2': bins[stationID][1],'field3': bins[stationID][2],'key':tsKey })
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers) 
        response = conn.getresponse()
        print(response.status, response.reason)
        conn.close()
    except:
        print("connection failed")


def activateStation(tsKey, stationID, whichBin):
    '''
        Function for activating user selected bin from waste station GUI
            Will trigger the chosen bin to check if it's full, then set the internal funnelling sytem to the
            selected bin. The station's main lid will be actuated to open, then wait for user to dispose item.
            After which the station's lid will close and the new fullness status will be uploaded to ThingSpeak.
        
        Param whichBin: The specific bin in the station
                            1 = Garbage Bin
                            2 = Cans/Bottles Bin  
                            3 = Papers Bin
                            4 = Compost Bin

        Return: 1 = Success
                0 = Failure
                2 = Selected bin is full
    '''
    
    while True:
        
        if (whichBin in [1, 2, 3]):
            # retrive bins new fullness value
            readFromThingSpeak(stationID)
            bins[stationID][whichBin - 1] += 5
            # only update ThingSpeak if the Arduino actually returned a vlaue
            if bins[stationID][whichBin - 1] is not None:
                #write data to ThingSpeak
                thingSpeakReturn = writeToThingSpeak(tsKey, stationID)
                return 1 if bins[stationID][whichBin - 1] < 100 else 2
        else:
            if (DEBUG):
                print('Invalid bin entry\n')
            return 0
