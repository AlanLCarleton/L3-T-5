#!/usr/bin/env python3
import serial
import time
import json
import urllib.request

#Function to send ThingSpeak channel data
def writeToThingSpeak(field1):
    URL = 'https://api.thingspeak.com/update?api_key='
    KEY = 'BLT9N7F99578BAAM'  # Write API Key (Bin 1)
    HEADER = ('&field2=%d' % (field1))
    FULL_URL = URL + KEY + HEADER   #URL for the get request

    return urllib.request.urlopen(FULL_URL).read()

def readThingspeakData():
    URL = 'https://api.thingspeak.com/channels/1222563/feeds.json?'
    HEADER = '&results=1'
    FULL_URL = URL + HEADER   #URL for the get request

    return urllib.request.urlopen(FULL_URL).read()


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser.flush()

    while True:
        print("\nWhich test would you like to run?\n")
        print("(1) Test Station Normal Operation (after user performed selection)\n")
        print("(2) Test Station with Selected Bin Full\n")
        print("(menu) send anything else or press on board reset button\n")
        option = str(input())
        ser.write(option.encode('utf-8'))

        if (option == '1' or option == '2'): 
            ser.flush()
            while True:
                line = ser.readline().decode('utf-8')
                #only take non blank data from serial com
                if (line != ''):
                    try:
                        fullness = int(line)
                    except:
                        #we're done reading
                        break
                    print("Distance from Ultrasonic Sensor: %dcm" % fullness)
                    #write data to ThingSpeak (arbitrary values for bins 1, 2, 3)
                    #writeToThingSpeak(fullness)
