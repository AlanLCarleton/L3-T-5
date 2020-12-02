#!/usr/bin/env python3
import serial
import urllib.request

'''
    Script for calling the microcontroller (Arduino) vis Serial
    Request to Arduino is for selecting which bin to activate for operation

    writeToThingSpeak   Function for writing data to specified ThingSpeak channel
    activateStation     Function to call for triggering a selected bin for operation
    testStation         Function for testing the station's bins.
'''

#Set this to True to have the fullness value be printed
DEBUG = True


def writeToThingSpeak(tsKey, binNum, fullness):
    '''
        Function to send data to specific ThingSpeak channel

        Param tsKey: The ThingSpeak channel API key that's being used
        Param binNum: The specific bin in the station
        Param fullness: The fullness value of the bin

        Return: ThingSpeak URL GET request
    '''
    URL = 'https://api.thingspeak.com/update?api_key='
    #tsKey = 'BLT9N7F99578BAAM'  # Write API Key (Station 1)
    fieldNum = 'field' + str(binNum+1)
    HEADER = ('&%s=%d' % (fieldNum, fullness))
    #print(HEADER)
    FULL_URL = URL + tsKey + HEADER  # URL for the get request

    return urllib.request.urlopen(FULL_URL).read()


def activateStation(tsKey, whichBin):
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
        if (whichBin in [1, 2, 3, 4]):
            # retrive bins new fullness value
            fullness = arduinoComm(whichBin)
            # only update ThingSpeak if the Arduino actually returned a vlaue
            if fullness is not None:
                #write data to ThingSpeak
                thingSpeakReturn = writeToThingSpeak(tsKey, int(whichBin), fullness)
                if (DEBUG):
                    print("Distance from Ultrasonic Sensor: %dcm" % fullness)
                    print("Return from ThingSpeak write:\n", thingSpeakReturn)
                
                return 1 if fullness < 100 else 2
        else:
            if (DEBUG):
                print('Invalid bin entry\n')
            return 0


def testStation():
    '''
        Function for testing activation of waste station's bins
            Options to choose which bin to test will be displayed. After entering a selection.
            the chosen bin will be triggered to check if it's full, then set the internal funnelling sytem to the
            selected bin. The station's main lid will be actuated to open, then wait for user to dispose item.
            After which the station's lid will close.

        Return: 1 = Success
    '''
    ser.flush()
    
    while True:
        print("\nWhich bin in the station would you like to use?\n")
        print("(1) Garbage Bin")
        print("(2) Cans/Bottles Bin")
        print("(3) Papers Bin")
        print("(4) Compost Bin")
        print("(5) To Exit Test\n")

        whichBin = str(input())

        if (whichBin in ['1', '2', '3', '4']):
            # retrive bins new fullness value
            fullness = arduinoComm(whichBin)

            if fullness is not None:
                print("Distance from Ultrasonic Sensor: %dcm" % fullness)
        elif (whichBin == '5'):
            print("Exiting test function...\n")
            return 1
        else: print ("Invalid menu choice. Please selected one of the following below:\n")


def arduinoComm(whichBin):
    '''
        Function for communication with Arduino via Serial connection
            Sends data (commands) to the Arduino in which the Arduino will
            send back results (fullness value).
        
        Param whichBin: The specific bin in the station
                            1 = Garbage Bin
                            2 = Cans/Bottles Bin  
                            3 = Papers Bin
                            4 = Compost Bin

        Return: fullness The new fullness value of the bin after performing its operation
    '''
    #write value to Arduino via serial
    ser.write(str(whichBin).encode('utf-8'))
    ser.flush()

    fullness = None
    while True:
        #read value from Arduino
        line = ser.readline().decode('utf-8')
        #only take non blank data from serial com
        if (line != ''):
            try:
                fullness = int(line)
            except:
                #if value from Arduin is not an int, then we're done reading
                break
            
    return fullness

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)
ser.flush()
