import urllib.request
import requests
import threading
import json
import sqlite3
from time import sleep
from maintenance_email import send_alert

# keys of three channals
stationNumber2channelID_key = {1: ['1222563','MG9FWWZOG8M0PCGK'], 2: ['1222564','TICC7ZFTEDZOPZ4F'], 3: ['1222565','A6YJ6ETTQ38WWHBN']}

# last retrieved levels of three waste stations
lastLevels = [[0,0,0],[0,0,0],[0,0,0]]

def get_levels(stationNumber):
    URL="https://api.thingspeak.com/channels/" + stationNumber2channelID_key[stationNumber][0] + "/feeds.json?api_key="
    KEY=stationNumber2channelID_key[stationNumber][1]
    HEADER='&results=1'
    NEW_URL=URL+KEY+HEADER
    get_data=requests.get(NEW_URL).json()

    feeds=get_data['feeds'][0]
    print(feeds)
    
    currentLevel = [int(feeds["field1"]),int(feeds["field2"]),int(feeds["field3"])]

    dbconnect = sqlite3.connect("maintenanceDB.db");
    dbconnect.row_factory = sqlite3.Row;
    cursor = dbconnect.cursor();
    if (lastLevels[stationNumber-1] != currentLevel):

        for i ,level in enumerate(currentLevel):
            if level >= 90:
                send_alert(i+1,stationNumber,level)

        lastLevels[stationNumber-1] = currentLevel
        cursor.execute('''insert into StationStatus values (?, ?, ?, ?)''', (stationNumber, feeds["field1"],feeds["field2"],feeds["field3"]))
        dbconnect.commit();


def start():
    while True:
        get_levels(1)
        sleep(1)
        get_levels(2)
        sleep(1)
        get_levels(3)
        sleep(1)

    
if __name__ == '__main__':
    start()

