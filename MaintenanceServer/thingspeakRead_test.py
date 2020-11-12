import urllib.request
import requests
import threading
import json


stationNumber2channelID_key = {1: ['1222563','MG9FWWZOG8M0PCGK'], 2: ['1222564','TICC7ZFTEDZOPZ4F'], 3: ['1222565','A6YJ6ETTQ38WWHBN']}


def get_level(stationNumber):
    URL="https://api.thingspeak.com/channels/" + stationNumber2channelID_key[stationNumber][0] + "/feeds.json?api_key="
    KEY=stationNumber2channelID_key[stationNumber][1]
    HEADER='&results=1'
    NEW_URL=URL+KEY+HEADER
    get_data=requests.get(NEW_URL).json()

    feeds=get_data['feeds'][0]
    print("Bin1:" + feeds["field2"])
    print("Bin2:" + feeds["field3"])
    print("Bin3:" + feeds["field4"])

def start_test():
    while True:
        print("Which Station?")
        inputNum = int(input())
        if(inputNum == 0):
            break
        
        print("Bin levels at Waste Station" + str(inputNum))
        get_level(inputNum)
            

    
if __name__ == '__main__':
    start_test()

