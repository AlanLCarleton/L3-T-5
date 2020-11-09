import urllib.request
import requests
import threading
import json


def read_level(channelID):
    URL="https://api.thingspeak.com/channels/" + str(channelID) + "/feeds.json?api_key="
    KEY='MG9FWWZOG8M0PCGK'
    HEADER='&results=1'
    NEW_URL=URL+KEY+HEADER
    print(NEW_URL)

    get_data=requests.get(NEW_URL).json()

    feeds=get_data['feeds'][0]
    
    print(feeds)

    print(feeds["field2"])
    print(feeds["field3"])
    print(feeds["field4"])
    
    
if __name__ == '__main__':
    read_level(1222563)

