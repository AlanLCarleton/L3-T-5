import urllib.request
import requests
import threading
import json
import sqlite3
from time import sleep

# keys of three channals
stationChannelID_key = {0: ['1222563','MG9FWWZOG8M0PCGK'], 1: ['1222564','TICC7ZFTEDZOPZ4F'], 2: ['1222565','A6YJ6ETTQ38WWHBN']}

# last retrieved levels of three waste stations
lastLevels = {0: [0,0,0], 1: [0,0,0], 2: [0,0,0]}

def get_levels(stationNumber, verbose):
    URL="https://api.thingspeak.com/channels/" + stationChannelID_key[stationNumber][0] + "/feeds.json?api_key="
    KEY=stationChannelID_key[stationNumber][1]
    HEADER='&results=1'
    NEW_URL=URL+KEY+HEADER
    get_data=requests.get(NEW_URL).json()

    feeds=get_data['feeds'][0]
    if verbose:
        print(feeds)
    
    currentLevel = [int(feeds["field1"]),int(feeds["field2"]),int(feeds["field3"])]
    if verbose:
        print (currentLevel)
    
    dbconnect = sqlite3.connect("maintenanceDB.db");
    dbconnect.row_factory = sqlite3.Row;
    cursor = dbconnect.cursor();
    
    if (lastLevels[stationNumber] != currentLevel):
        lastLevels[stationNumber] = currentLevel
        cursor.execute('''insert into StationStatus values (?, ?, ?, ?)''', (stationNumber, feeds["field1"],feeds["field2"],feeds["field3"]))
        dbconnect.commit();
    print("Latest values in database")
    print (str(stationNumber) + ": " + str(lastLevels[stationNumber]))
    if verbose:
        print("Current maintenance database:")
    cursor.execute('SELECT * FROM StationStatus');
    #print data
    if verbose:
        for row in cursor:
            print(row['StationLocation'],row['Bin1'],row['Bin2'],row['Bin3']);
        
    dbconnect.close();

def start_test():
    while True:
        get_levels(0, True)
        sleep(1)
        get_levels(1, True)
        sleep(1)
        get_levels(2, True)
        sleep(1)

def get_last_levels():
    get_levels(0, False)
    get_levels(1, False)
    get_levels(2, False)
    
    return lastLevels
            

    
if __name__ == '__main__':
    start_test()

