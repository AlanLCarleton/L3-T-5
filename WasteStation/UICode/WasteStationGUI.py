try:
    import Tkinter as tk
except:
    import tkinter as tk

import time
import sys
import http.client
import urllib.parse
import urllib.request
import requests
sys.path.insert(1, '../SensorControls')

SIMULATOR = False
if SIMULATOR:
    import hardwareEmulator
else:
    import runStation

subway_items = ["Plastic Bag", "Sandwich Wrap", "Hot Cup", "Salad Bowl", "Napkins", "Cookie Bag"]
subway_bins = [0, 1, 1, 2, 1, 1] 
tim_hortons_items = ["Hot Drink Cup", "Cold Drink Cup", "Soup Bowl", "Lid", "Tray", "Plastic Bottle"]
tim_hortons_bins = [1, 2, 1, 0, 1, 2]
pizza_pizza_items = ["Pizza Box", "Pizza Slice Holder", "Napkins", "Wings Box", "Sauce Container", "Fries Box"]
pizza_pizza_bins = [1, 1, 1, 1, 0, 1]

bin_strings = ["Waste", "Paper", "Plastics"]
bin_full_list = [[False, False, False], [False, False, False], [False, False, False]]


station_id = 1
#write_channel_key = 'BLT9N7F99578BAAM'
write_channel_key = 'GDHEA7VGR18FXYSU'
#write_channel_key ='KBQ5HYT7A32U1TQK'
channelID = 1222563
channelID += station_id

class Test():
    
    def getEmptyBinLocations(self, stationID):
        #channelID = 1222563
        #channelID += stationID
        URL="https://api.thingspeak.com/channels/" + str(channelID) + "/feeds.json?api_key="
        KEY='MG9FWWZOG8M0PCGK'
        HEADER='&results=1'
        NEW_URL=URL+KEY+HEADER
        try:
            station_data=requests.get(NEW_URL).json()
        except:
            print("Failure: No response")
            return False

        feeds = station_data['feeds'][0]

        if(int(feeds["field1"]) >= 95):
            bin_full_list[stationID][0] = True
        else:
            bin_full_list[stationID][0] = False
            
        if(int(feeds["field2"]) >= 95):
            bin_full_list[stationID][1] = True
        else:
            bin_full_list[stationID][1] = False
            
        if(int(feeds["field3"]) >= 95):
            bin_full_list[stationID][2] = True
        else:
            bin_full_list[stationID][2] = False
        
        
    def chooseBin(self, channelID, binID):
        # Value checking for binID and stationID
        if(not isinstance(binID, int) or not isinstance(station_id, int)):# Checks that binID and stationID are int
            return False
        if(binID < 0 or binID >= 3): # Only 0 to 2 are valid bin IDs
            return False
        
        self.getEmptyBinLocations(station_id)
        if bin_full_list[station_id][binID]:
            next_station_id = (station_id + 1) % 3 
            self.getEmptyBinLocations(next_station_id)
            if bin_full_list[next_station_id][binID] == False:
                self.label.config(text = "Bin is full! Waste Station "+ str(next_station_id) + " has a non-full bin you can use :)")
                return False
            next_station_id = (station_id + 2) % 3 
            self.getEmptyBinLocations(next_station_id)
            if bin_full_list[next_station_id][binID] == False:
                self.label.config(text = "Bin is full! Waste Station "+ str(next_station_id) + " has a non-full bin you can use :)")
                return False
            self.label.config(text = "Bin is full! All other Waste Stations also have full bins :(")
            return False
            
        
        if SIMULATOR:
            result = hardwareEmulator.activateStation(write_channel_key, station_id, binID)
        else:
            result = runStation.activateStation(write_channel_key, channelID, binID)
        
        #Bin did not succesfully open
        if(result == 0):
            print("Something went wrong. Please try again.")
            time.sleep(2)
            return False
        #Bin successfully opens
        elif(result == 1):
            return True
            
    
    def select_item(self, itemNum):
        self.item0Button.grid_remove()
        self.item1Button.grid_remove()
        self.item2Button.grid_remove()
        self.item3Button.grid_remove()
        self.item4Button.grid_remove()
        self.item5Button.grid_remove()
        if self.current_restaurant == "Subway":
            bin_num = subway_bins[itemNum]
            binName = bin_strings[bin_num]
        if self.current_restaurant == "Tim Hortons":
            bin_num = tim_hortons_bins[itemNum]
            binName = bin_strings[bin_num]
        if self.current_restaurant == "Pizza Pizza":
            bin_num = pizza_pizza_bins[itemNum]
            binName = bin_strings[bin_num]
        self.label.config(text = "Opening " + binName + " bin!")
        self.chooseBin(channelID, bin_num)
        self.backButton.config(text = "Close Bin")
    
    def open_restaurant(self, restaurantName):
        self.current_restaurant = restaurantName
        self.subwayButton.grid_remove()
        self.timHortonsButton.grid_remove()
        self.pizzaPizzaButton.grid_remove()
        self.item0Button.grid()
        self.item1Button.grid()
        self.item2Button.grid()
        self.item3Button.grid()
        self.item4Button.grid()
        self.item5Button.grid()
        if self.current_restaurant == "Subway":
            self.item0Button.config(text = subway_items[0])
            self.item1Button.config(text = subway_items[1])
            self.item2Button.config(text = subway_items[2])
            self.item3Button.config(text = subway_items[3])
            self.item4Button.config(text = subway_items[4])
            self.item5Button.config(text = subway_items[5])
        if self.current_restaurant == "Tim Hortons":
            self.item0Button.config(text = tim_hortons_items[0])
            self.item1Button.config(text = tim_hortons_items[1])
            self.item2Button.config(text = tim_hortons_items[2])
            self.item3Button.config(text = tim_hortons_items[3])
            self.item4Button.config(text = tim_hortons_items[4])
            self.item5Button.config(text = tim_hortons_items[5])
        if self.current_restaurant == "Pizza Pizza":
            self.item0Button.config(text = pizza_pizza_items[0])
            self.item1Button.config(text = pizza_pizza_items[1])
            self.item2Button.config(text = pizza_pizza_items[2])
            self.item3Button.config(text = pizza_pizza_items[3])
            self.item4Button.config(text = pizza_pizza_items[4])
            self.item5Button.config(text = pizza_pizza_items[5])
        
        self.label.config(text = "Choose an item from " + restaurantName)
        
    def open_bin(self, binName):
        self.wasteBinButton.grid_remove()
        self.paperBinButton.grid_remove()
        self.plasticsBinButton.grid_remove()
        self.label.config(text = "Opening " + binName + " bin!")
        bin_num = bin_strings.index(binName)
        self.chooseBin(channelID, bin_num)
        self.backButton.config(text = "Close Bin")
        
    def bins(self):
        self.backButton.grid()
        self.wasteBinButton.grid()
        self.paperBinButton.grid()
        self.plasticsBinButton.grid()
        self.label.config(text = "Please select a bin")
        self.binsButton.grid_remove()
        self.itemsButton.grid_remove()
       
    def items(self):
        self.backButton.grid()
        self.label.config(text = "Please choose a restaurant")
        self.binsButton.grid_remove()
        self.itemsButton.grid_remove()
        self.subwayButton.grid()
        self.timHortonsButton.grid()
        self.pizzaPizzaButton.grid()
       
    def back(self):
        self.label.config(text = "Please choose to open a bin or select an item")
        self.backButton.config(text = "Back")
        self.backButton.grid_remove()
        self.wasteBinButton.grid_remove()
        self.paperBinButton.grid_remove()
        self.plasticsBinButton.grid_remove()
        self.subwayButton.grid_remove()
        self.timHortonsButton.grid_remove()
        self.pizzaPizzaButton.grid_remove()
        self.binsButton.grid()
        self.itemsButton.grid()
        self.item0Button.grid_remove()
        self.item1Button.grid_remove()
        self.item2Button.grid_remove()
        self.item3Button.grid_remove()
        self.item4Button.grid_remove()
        self.item5Button.grid_remove()
        
    def __init__(self):
        self.current_restaurant = ""
        self.root = tk.Tk()
        self.label=tk.Label(self.root,
                           text = "Please choose to open a bin or select an item")
        self.binsButton = tk.Button(self.root,
                          text = 'Bins',
                          command=self.bins)
        self.itemsButton = tk.Button(self.root,
                          text = 'Items',
                          command=self.items)
        self.backButton = tk.Button(self.root,
                          text = 'Back',
                          command=self.back)
        self.wasteBinButton = tk.Button(self.root,
                          text = 'Waste',
                          command = lambda: self.open_bin(binName="Waste"))
        self.paperBinButton = tk.Button(self.root,
                          text = 'Paper',
                          command = lambda: self.open_bin(binName="Paper"))
        self.plasticsBinButton = tk.Button(self.root,
                          text = 'Plastics',
                          command = lambda: self.open_bin(binName="Plastics"))
        self.subwayButton = tk.Button(self.root,
                          text = 'Subway',
                          command = lambda: self.open_restaurant(restaurantName="Subway"))
        self.timHortonsButton = tk.Button(self.root,
                          text = 'Tim Hortons',
                          command = lambda: self.open_restaurant(restaurantName="Tim Hortons"))
        self.pizzaPizzaButton = tk.Button(self.root,
                          text = 'Pizza Pizza',
                          command = lambda: self.open_restaurant(restaurantName="Pizza Pizza"))
        self.item0Button = tk.Button(self.root,
                          text = 'Item1',
                          command = lambda: self.select_item(itemNum = 0))
        self.item1Button = tk.Button(self.root,
                          text = 'Item1',
                          command = lambda: self.select_item(itemNum = 1))
        self.item2Button = tk.Button(self.root,
                          text = 'Item1',
                          command = lambda: self.select_item(itemNum = 2))
        self.item3Button = tk.Button(self.root,
                          text = 'Item1',
                          command = lambda: self.select_item(itemNum = 3))
        self.item4Button = tk.Button(self.root,
                          text = 'Item1',
                          command = lambda: self.select_item(itemNum = 4))
        self.item5Button = tk.Button(self.root,
                          text = 'Item1',
                          command = lambda: self.select_item(itemNum = 5))
        self.label.grid(row = 0, column = 0, columnspan = 3)
        self.binsButton.grid(row = 1, column = 0)
        self.itemsButton.grid(row = 1, column = 1)
        self.backButton.grid(row = 3, column = 0, columnspan = 3)
        self.wasteBinButton.grid(row = 1, column = 0)
        self.paperBinButton.grid(row = 1, column = 1)
        self.plasticsBinButton.grid(row = 1, column = 2)
        self.subwayButton.grid(row = 1, column = 0)
        self.timHortonsButton.grid(row = 1, column = 1)
        self.pizzaPizzaButton.grid(row = 1, column = 2)
        self.item0Button.grid(row = 1, column = 0)
        self.item1Button.grid(row = 1, column = 1)
        self.item2Button.grid(row = 1, column = 2)
        self.item3Button.grid(row = 2, column = 0)
        self.item4Button.grid(row = 2, column = 1)
        self.item5Button.grid(row = 2, column = 2)
        self.backButton.grid_remove()
        self.wasteBinButton.grid_remove()
        self.paperBinButton.grid_remove()
        self.plasticsBinButton.grid_remove()
        self.subwayButton.grid_remove()
        self.timHortonsButton.grid_remove()
        self.pizzaPizzaButton.grid_remove()
        self.item0Button.grid_remove()
        self.item1Button.grid_remove()
        self.item2Button.grid_remove()
        self.item3Button.grid_remove()
        self.item4Button.grid_remove()
        self.item5Button.grid_remove()
        
        w = 500 # width for the Tk root
        h = 500 # height for the Tk root

        # get screen width and height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.mainloop()
       
    
       
    def quit(self):
       self.root.destroy()
        
app = Test()