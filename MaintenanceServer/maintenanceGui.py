from sense_hat import SenseHat
import time
import urllib.request
import requests
import threading
import json

sense = SenseHat()

# Preset RGB values. Odd behaviour occured when using get_pixel(). If pixel is set at (255,0,0), will be read back as (248,0,0).
# Presets were changed to use 248 instead of 255.
green = (0, 248, 0)
red = (248, 0, 0)
blue = (0, 0, 248)
white = (248, 252, 248)

# Thingspeak Station IDs
station0_id=1222563
station1_id=1222564
station2_id=1222565

station_ids = [station0_id, station1_id, station2_id]
station_index = 0
num_stations = len(station_ids)

# Bin types
bin_index = 0
bins = ["waste", "paper", "plastics", "cans"]
num_bins = len(bins)

# Volume of bins in percentage (0-100%)
waste_volume = 0
paper_volume = 0
plastics_volume = 0
cans_volume = 0

# Sets a percentage of pixels on screen equal to percentage of volume filled in bin.
# Does not change colour of pixel that is part of letter
def show_volume(volume):
  # Convert volume from percentage to number of pixels
  volume_value = round((int(volume) / 100) * 64)
  for x in range(8):
    for y in range(8):
      # If pixel isn't part of the letter (checks if red)
      if not sense.get_pixel(x, y) == [248, 0, 0]:
        # Calculates which pixel we are at. Sense HAT uses the top row as y = 0, y gets flipped so the bottom row is y = 0. This simplifies the math.
        position_value = (abs(y-7) * 8) + x
        # If we haven't reached the max pixel, set to green. Otherwise, set to white.
        if position_value < volume_value:
          sense.set_pixel(x,y,green)
        else:
          sense.set_pixel(x,y,white)

def show_c():
  sense.show_letter("C", text_colour=red)
  
def show_p():
  sense.show_letter("P", text_colour=red)
  
def show_l():
  sense.show_letter("L", text_colour=red)

def show_w():
  sense.show_letter("W", text_colour=red)

# Set pixels to show letter for bin and volume
def update_screen(mode):
  if mode == "waste":
    show_w()
    show_volume(waste_volume)
  elif mode == "paper":
    show_p()
    show_volume(paper_volume)
  elif mode == "plastics":
    show_l()
    show_volume(plastics_volume)
  elif mode == "cans":
    show_c()
    show_volume(cans_volume)

# Show what bin we are viewing
def show_station_index(index):
  sense.show_letter(str(index), text_colour=red, back_colour=green)

# Read Bin volume information from ThingSpeak
def read_level(channelID):
  URL="https://api.thingspeak.com/channels/" + str(channelID) + "/feeds.json?api_key="
  KEY='MG9FWWZOG8M0PCGK'
  HEADER='&results=1'
  NEW_URL=URL+KEY+HEADER

  get_data=requests.get(NEW_URL).json()

  feeds=get_data['feeds'][0]
  global waste_volume, paper_volume, plastics_volume
  waste_volume = feeds["field2"]
  paper_volume = feeds["field3"]
  plastics_volume = feeds["field4"]

# Main exeution loop
show_station_index(station_index % num_stations)
time.sleep(1)
read_level(station0_id)
update_screen("waste")

while True:
  selection = False
  events = sense.stick.get_events()
  for event in events:
    if event.action != "released":
      if event.direction == "left":
        bin_index -= 1
        current_mode = bins[bin_index % num_bins]
        update_screen(current_mode)
      elif event.direction == "right":
        bin_index += 1
        current_mode = bins[bin_index % num_bins]
        update_screen(current_mode)
      elif event.direction == "up":
        station_index += 1
        show_station_index(station_index % num_stations)
        read_level(station_ids[station_index % num_stations])
      elif event.direction == "down":
        station_index -= 1
        show_station_index(station_index % num_stations)
        read_level(station_ids[station_index % num_stations])
       
        
  
  