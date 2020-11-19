import time

#The value of binID corresponds to each of the three bins in the system.
#1 = Garbage, 2 = Plastics, 3 = Papers
def chooseBin(binID):
	#The following is placeholder code until servo is integrated with UI
	if(binID == 1):
		print("Accessing Garbage bin")
		time.sleep(2)
		print("Garbage bin is open. Please begin depositing.")
		time.sleep(2)	
		return True
	elif(binID == 2):
		print("Accessing Plastics bin")
		time.sleep(2)
		print("Plastics bin is open. Please begin depositing.")
		time.sleep(2)
		return True
	elif(binID == 3):
		print("Accessing Paper bin")
		time.sleep(2)
		print("Paper bin is open. Please begin depositing.")
		time.sleep(2)
		return True
	else:
		print("Provided Bin ID is invalid")
		return False

#returns bin location if bin level is below 100, else it returns 
def getEmptyBinLocation(channel_key, channel_id, bin_id):
	if(not isinstance(bin_id, int)):# Checks that bin_id is an int
		return False
	if(bin_id < 1 or bin_id > 3): # Only 1 to 3 are valid bin IDs
		return False	

	URL="https://api.thingspeak.com/channels/" + str(channel_id) + "/feeds.json?api_key=" 
	KEY=channel_key
	HEADER='&results=1'
	NEW_URL=URL+KEY+HEADER

	get_data=requests.get(NEW_URL).json()
	
	feeds = get_data['feeds'][0]

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
			binID = int(input())
			chooseBin(binID)

		#Determine bin by searching for item
		elif(option == 2):
			while True:
				print("Select an item:")
				for x in itemList: # Display all of the items in the list
					print(x)
				itemName = str(input())

				if itemName in itemList:
					chooseBin(itemList[itemName])
					break;
				else:
					print("That is an invalid input")
					time.sleep(2)
		else:
			print("Invalid Input")