import urllib.request
import requests
import threading
import json


def read_data_thingspeak():
    URL='https://api.thingspeak.com/channels/1158535/fields/1.json?api_key='
    KEY='RAKH5HJNI61IOO4B'
    HEADER='&results=2'
    NEW_URL=URL+KEY+HEADER
    print(NEW_URL)

    get_data=requests.get(NEW_URL).json()
    #print(get_data)
    #channel_id=get_data['channel']['id']

    feeds=get_data['feeds']
    #print(feeds)

    t=[]
    
    for feed in feeds:
        print(feed['field1'])
        t.append(feed['field1'])
    
    print(t)

if __name__ == '__main__':
    read_data_thingspeak()

