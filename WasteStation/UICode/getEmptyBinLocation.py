import http.client
import json
import time
import requests

#returns bin location if bin level is below 100, else it returns 
def getEmptyBinLocation(channel_key, channel_id, bin_id):
	URL="https://api.thingspeak.com/channels/" + str(channel_id) + "/feeds.json?api_key=" 
	KEY=channel_key
	HEADER='&results=1'
	NEW_URL=URL+KEY+HEADER

	get_data=requests.get(NEW_URL).json()
	
	feeds = get_data['feeds'][0]
	
	#The bing_id value must be incremented by 1 because of the offset from the id and the assigned Thingspeak field
	bin_id += 1
	field_str = "field" + str(bin_id)

	if(int(feeds[field_str]) < 90):
		#return feeds["field1"]
		return True
	else:
		#return None
		return False

if __name__ == '__main__':
	channelID = 1222563
	channelKey = "BLT9N7F99578BAAM"

	while True:
		print("Please select a bin.\n")
		print("(1) for Garbage\n")
		print("(2) for Plastic\n")
		print("(3) for Paper\n")
		print("(0) to Quit\n")
		option = int(input())
		
		if(option == 0):
			print("Shutting down")
			break

		elif(option == 1):
			print("Accessing Garbage bin\n")
			time.sleep(1)
			print("Garbage bin is full. Searching for available stations.\n")
			
			if(getEmptyBinLocation(channelKey, channelID, option)):
				print("a Garbage bin is available at Waste Station 1\n")
			else:
				print("There are currently no Garbage bins available\n")
			time.sleep(1)

		elif(option == 2):
			print("Accessing Plastic bin\n")
			time.sleep(1)
			print("Plastic bin is full. Searching for available stations.\n")
			
			if(getEmptyBinLocation(channelKey, channelID, option)):
				print("a Plastic bin is available at Waste Station 1\n")
			else:
				print("There are currently no Plastic bins available\n")
			time.sleep(1)

		elif(option == 3):
			print("Accessing Paper bin\n")
			time.sleep(1)
			print("Paper bin is full. Searching for available stations.\n")
			
			if(getEmptyBinLocation(channelKey, channelID, option)):
				print("a Paper bin is available at Waste Station 1\n")
			else:
				print("There are currently no Paper bins available\n")
			time.sleep(1)

		else:
			print("Invalid Input")
