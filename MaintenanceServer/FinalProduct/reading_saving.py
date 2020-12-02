import urllib.request
import requests
import threading
import json
import sqlite3
from time import sleep

# keys of three channals
stationNumber2channelID_key = {1: ['1222563','MG9FWWZOG8M0PCGK'], 2: ['1222564','TICC7ZFTEDZOPZ4F'], 3: ['1222565','A6YJ6ETTQ38WWHBN']}

# last retrieved levels of three waste stations
lastLevels = {1:[0,0,0], 2:[0,0,0],3:[0,0,0]}

def get_levels(stationNumber):
    URL="https://api.thingspeak.com/channels/" + stationNumber2channelID_key[stationNumber][0] + "/feeds.json?api_key="
    KEY=stationNumber2channelID_key[stationNumber][1]
    HEADER='&results=1'
    NEW_URL=URL+KEY+HEADER
    get_data=requests.get(NEW_URL).json()

    feeds=get_data['feeds'][0]
    print(feeds)
    
    currentLevel = [int(feeds["field2"]),int(feeds["field3"]),int(feeds["field4"])]
    print (lastLevels[stationNumber])
    print (currentLevel)
    
    dbconnect = sqlite3.connect("maintenanceDB.db");
    dbconnect.row_factory = sqlite3.Row;
    cursor = dbconnect.cursor();
    if (lastLevels[stationNumber] != currentLevel):
        lastLevels[stationNumber] = currentLevel
        cursor.execute('''insert into StationStatus values (?, ?, ?, ?)''', (stationNumber, feeds["field2"],feeds["field3"],feeds["field4"]))
        dbconnect.commit();

    print("Current maintenance database:")
    cursor.execute('SELECT * FROM StationStatus');
    #print data
    for row in cursor:
        print(row['StationLocation'],row['Bin1'],row['Bin2'],row['Bin3']);
        
    dbconnect.close();

def start_test():
    while True:
        get_levels(1)
        sleep(1)
        get_levels(2)
        sleep(1)
        get_levels(3)
        sleep(1)
            

    
if __name__ == '__main__':
    start_test()

