import sys
sys.path.insert(1, '../SensorControls')
import time
import runStation

#The value of binID corresponds to each of the three bins in the system.
#1 = Garbage, 2 = Plastics, 3 = Papers, 4 = Compost
def chooseBin(binID, stationID):
	#Dictionary containing the channel id and API key of each station
	stationData = {
		1 : {'channel_key' : 'MG9FWWZOG8M0PCGK', 'channel_id': '1222563'},
		2 : {'channel_key' : 'TICC7ZFTEDZOPZ4F', 'channel_id': '1222564'},
		3 : {'channel_key' : 'A6YJ6ETTQ38WWHBN', 'channel_id': '1222565'}
	}
	result = activateStation(stationData[stationID]['channel_key'], binID)
	
	#Bin did not succesfully open
	if(result == 0):
		print("Something went wrong. Please try again.")
		time.sleep(3)
	#Bin successfully opens
	elif(result == 1):
		print("Please begin depositing")
		time.sleep(5)
	#Selected bin is full
	elif(result == 2):
		print("This bin is currently full")
		for x in stationData:
			if(x != stationID):
				if(getEmptyBinLocation(stationData[stationID]['channel_key'], stationData[stationID]['channel_id'], binID)):
					print("This bin is currently available at Waste Station" + str(x))
			

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

	feeds = station_data['feeds'][0]

	#The bin_id value must be incremented by 1 because of the offset from the id and the corresponding Thingspeak field
	field_id = bin_id + 1
	field_str = "field" + str(field_id)

	if(int(feeds[field_str]) <= 90):
		#return feeds["field1"]
		return True
	else:
		#return None
		return False


if __name__ == '__main__':

	#Each item follows the format of "Item name":"Bin ID"
	itemList = {
		"Bottle" : 2,
		"Can" : 2,
		"Food" : 1,
		"Cardboard Container" : 3
	}

	print("Input Station #:")
	stationID = int(input())
	while True:
		print("Select an Option:")
		print("(1) to select a bin")
		print("(2) to search for an item")
		option = int(input())
		
		#Directly access a selected bin 
		if(option == 1):
			print("Please select a bin.")
			print("(1) for Garbage")
			print("(2) for Plastic")
			print("(3) for Paper")
			print("(0) to go back")
			binID = int(input())
			if(bin_id != 0):
				chooseBin(binID, stationID)

		#Determine bin by searching for item
		elif(option == 2):
			while True:
				print("Select an item:")
				for x in itemList: # Display all of the items in the list
					print(x)
				print("Enter 'exit' to go back")
				itemName = str(input())

				if itemName in itemList:
					chooseBin(itemList[itemName], stationID)
					break;
				elif(itemName == "exit"):
					break;
				else:
					print("That is an invalid input")
					time.sleep(2)
		else:
			print("Invalid Input")