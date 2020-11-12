#!/usr/bin/env python3
import serial
import time
import json
import urllib.request

#Function to send ThingSpeak channel data
def writeToThingSpeak(field1, field2, field3):
    URL = 'https://api.thingspeak.com/update?api_key='
    KEY = 'BLT9N7F99578BAAM'  # Write API Key (Bin 1)
    HEADER = ('&field2=%d&field3=%d&field4=%d' % (field1, field2, field3))
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
        print("\nWhich component would you like to test?\n")
        print("(1) Ultrasonic Sensor - HC-SR04 (Tests Writing to ThingSpeak)\n")
        print("(2) Test Reading From to ThingSpeak\n")
        print("(3) Stepper Motor\n")
        print("(4) FS90R Servo Motor\n")
        print("(menu) send anything else or press on board reset button\n")
        option = str(input())
        ser.write(option.encode('utf-8'))

        if (option == '1'): #Writing UltraSonic sensor data
            ser.flush()
            while True:
                line = ser.readline().decode('utf-8').rstrip()
                #only take non blank data from serial com
                if (line != ''):
                    try:
                        fullness = int(line)
                    except:
                        #we're done reading
                        break
                    print("Distance from Ultrasonic Sensor: %dcm" % fullness)
                    #write data to ThingSpeak (arbitrary values for bins 1, 2, 3)
                    writeToThingSpeak(fullness, fullness+5, fullness-5)
        elif (option == '2'): #Reading bin fullness from ThingSPeak
            startTime = time.time()
            while True:
                #run this test for 18s
                if (time.time() >= startTime + 18): break
                data = json.loads(readThingspeakData())
                print("Successfully read data from ThingSpeak")
                feeds = data['feeds']    #extract from the pairs of feeds (only 1 in this case)
                #Extract data from each feed
                field2 = feeds[0]['field2']
                field3 = feeds[0]['field3']
                field4 = feeds[0]['field4']
                print('Field2=%s Field3=%s Field4=%s' % (field2, field3, field4))
                time.sleep(5) #read every 5s
