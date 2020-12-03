import sys
sys.path.insert(1, '../SensorControls')
import time
import runStation

#The value of binID corresponds to each of the three bins in the system.
#1 = Garbage, 2 = Plastics, 3 = Papers, 4 = Compost
def chooseBin(binID, stationID):
    #Dictionary containing the channel id and API key of each station
    stationData = {
        1 : {'channel_key' : 'BLT9N7F99578BAAM', 'channel_id': '1222563'},
        2 : {'channel_key' : 'GDHEA7VGR18FXYSU', 'channel_id': '1222564'},
        3 : {'channel_key' : 'KBQ5HYT7A32U1TQK', 'channel_id': '1222565'}
    }

    # Value checking for binID and staionID
    if(not isinstance(binID, int) or not isinstance(stationID, int)):# Checks that binID and stationID are int
        return False
    if(binID < 1 or binID > 4): # Only 1 to 4 are valid bin IDs
        return False
    if(stationID < 1 or stationID > 3): # Currently there are only 3 stations
        return False
    
    print("Starting process...")
    result = runStation.activateStation(stationData[stationID]['channel_key'], stationData[stationID]['channel_id'], binID)
    
    #Bin did not succesfully open
    if(result == 0):
        print("Something went wrong. Please try again.")
        time.sleep(3)
        return False
    #Bin successfully opens
    elif(result == 1):
        return True
    #Selected bin is full
    elif(result == 2):
        print("This bin is currently full")
        for x in stationData:
            if(x != stationID):
                if(getEmptyBinLocation(stationData[stationID]['channel_key'], stationData[stationID]['channel_id'], binID)):
                    print("This bin is currently available at Waste Station" + str(x))
        return True
            

#returns True if bin level is below 100, else it returns False
def getEmptyBinLocation(channel_key, channel_id, bin_id):
    if(not isinstance(bin_id, int)):# Checks that bin_id is an int
        return False
    if(bin_id < 1 or bin_id > 4): # Only 1 to 4 are valid bin IDs
        return False    

    URL="https://api.thingspeak.com/channels/" + channel_id + "/feeds.json?api_key=" 
    KEY=channel_key
    HEADER='&results=1'
    NEW_URL=URL+KEY+HEADER
    
    try:
        station_data=requests.get(NEW_URL).json()
    except:
        print("Failure: No response")
        return False

    feeds = station_data['feeds'][0]

    #The bin_id value must be incremented by 1 because of the offset from the id and the corresponding Thingspeak field
    field_id = bin_id + 1
    field_str = "field" + str(field_id)

    if(int(feeds[field_str]) <= 100):
        #return feeds["field1"]
        return True
    else:
        #return None
        return False
#Tests the input checking for UI functions. Does not handle sensors as they have their own tests
def testUIComponents():
    #Tests chooseBin function with proper inputs
    #assert chooseBin(1, 1) == True

    # Test invalid inputs to binID for chooseBin
    assert chooseBin(0, 1) == False
    assert chooseBin(5, 1) == False
    assert chooseBin("Garbage", 1) == False
    
    #Test invalid inputs to stationID for chooseBin
    assert chooseBin(1, 0) == False
    assert chooseBin(1, 4) == False
    assert chooseBin(1, "one") == False

    # Test invalid inputs to binID for getEmptyBinLocation
    assert getEmptyBinLocation('MG9FWWZOG8M0PCGK', 1222563, 1) == False
    assert getEmptyBinLocation('MG9FWWZOG8M0PCGK', 1222563, 1) == False
    assert getEmptyBinLocation('MG9FWWZOG8M0PCGK', 1222563, 1) == False

    print("Startup tests were successful")
    
if __name__ == '__main__':
    
    #testUIComponents()
    
    #Each item follows the format of "Item name":"Bin ID"
    itemList = {
        "Bottle" : 2,
        "Can" : 2,
        "Cardboard Container" : 3,
        "Food" : 1,
        "Green Waste" : 4
    }

    print("Input Station #:")
    stationID = int(input())
    while True:
        print("\nSelect an Option:")
        print("\t(1) to select a bin")
        print("\t(2) to search for an item")
        option = int(input())
        
        #Directly access a selected bin 
        if(option == 1):
            print("\nPlease select a bin.")
            print("\t(1) for Garbage")
            print("\t(2) for Plastic")
            print("\t(3) for Paper")
            print("\t(4) for Compost")
            print("\t(0) to go back")
            binID = int(input())
            if(binID != 0):
                if(chooseBin(binID, stationID)):
                    print("Returning to Option Select")
                    time.sleep(2)

        #Determine bin by searching for item
        elif(option == 2):
            while True:
                print("Select an item:")
                for x in itemList: # Display all of the items in the list
                    print('\t', x)
                print("\tEnter 'exit' to go back")
                itemName = str(input())

                if itemName in itemList:
                    if(chooseBin(itemList[itemName], stationID)):
                        print("Returning to Option Select")
                        time.sleep(2)
                    break;
                elif(itemName == "exit"):
                    break;
                else:
                    print("That is an invalid input")
                    time.sleep(2)
        else:
            print("Invalid Input")
