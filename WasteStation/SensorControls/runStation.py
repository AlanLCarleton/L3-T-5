#!/usr/bin/env python3
import serial
import time
import json
import urllib.request

'''
    Script for calling the microcontroller (Arduino) vis Serial
    Request to Arduino is for selecting which bin to activate for operation

    writeToThingSpeak   Function for writing data to specified ThingSpeak channel
    activateStation     Function to call for triggering a selected bin for operation
    testStation         Function for testing the station's bins.
'''


def writeToThingSpeak(tsKey, binNum, value):
    '''
        Function to send data to specific ThingSpeak channel

        Param tsKey: The ThingSpeak channel API key that's being used
        Param binNum: The specific bin in the station
        Param value: The fullness value of the bin

        Return: ThingSpeak URL GET request
    '''
    URL = 'https://api.thingspeak.com/update?api_key='
    #tsKey = 'BLT9N7F99578BAAM'  # Write API Key (Station 1)
    fieldNum = 'field' + str(binNum+1)
    HEADER = ('&%s=%d' % (fieldNum, value))
    print(HEADER)
    FULL_URL = URL + tsKey + HEADER  # URL for the get request

    return urllib.request.urlopen(FULL_URL).read()


DEBUG = False
def activateStation(tsKey, whichBin):
    '''
        Function for activating user selected bin from waste station GUI
            Will trigger the chosen bin to check if it's full, then set the internal funnelling sytem to the
            selected bin. The station's main lid will be actuated to open, then wait for user to dispose item.
            After which the station;s lid will close and the new fullness status will be uploaded to ThingSpeak.
        
        Param whichBin: The specific bin in the station
                            1 = Garbage Bin
                            2 = Cans/Bottles Bin  
                            3 = Papers Bin
                            4 = Compost Bin

        Return: 1 = Success
                0 = Failure
    '''
    ser.flush()

    while True:
        if (whichBin == 1 or whichBin == 2 or whichBin == 3 or whichBin == 4):
            ser.write(whichBin.encode('utf-8'))

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
                    #write data to ThingSpeak
                    thingSpeakReturn = writeToThingSpeak(tsKey, int(whichBin), fullness)
                    if (DEBUG):
                        print("Distance from Ultrasonic Sensor: %dcm" % fullness)
                        print("Return from ThingSpeak write:\n", thingSpeakReturn)
            return 1
        else:
            if (DEBUG):
                print('Invalid bin entry\n')
            
            return 0

def testStation():
    ser.flush()
    
    while True:
        print("\nWhich bin in the station would you like to use?\n")
        print("(1) Garbage Bin\n")
        print("(2) Cans/Bottles Bin\n")
        print("(3) Papers Bin\n")
        print("(4) Compost Bin\n")
        print("(5) To Exit Test\n")

        whichBin = str(input())
        ser.write(whichBin.encode('utf-8'))

        if (whichBin == '1' or whichBin == '2' or whichBin == '3' or whichBin == '4'):
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
        elif (whichBin == '5'):
            print("Exiting test function...\n")
            return 1
        else: print ("Invalid menu choice. Please selected one of the following below:\n")


ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
ser.flush()
