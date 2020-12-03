from sense_hat import SenseHat
import time
import urllib.request
import requests
import threading
import json
import smtplib, ssl
import time
import reading_saving

sense = SenseHat()

# Preset RGB values. Odd behaviour occured when using get_pixel(). If pixel is set at (255,0,0), will be read back as (248,0,0).
# Presets were changed to use 248 instead of 255.
green = (0, 248, 0)
red = (248, 0, 0)
blue = (0, 0, 248)
white = (248, 252, 248)

# Volume of bins in percentage (0-100%)
bin_0 = {
    "waste": 0,
    "paper": 0,
    "plastics": 0
    }
bin_1 = {
    "waste": 0,
    "paper": 0,
    "plastics": 0
    }
bin_2 = {
    "waste": 0,
    "paper": 0,
    "plastics": 0
    }
bins_list = [bin_0, bin_1, bin_2]

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
  
def show_p():
  sense.show_letter("P", text_colour=red)
  
def show_l():
  sense.show_letter("L", text_colour=red)

def show_w():
  sense.show_letter("W", text_colour=red)

# Set pixels to show letter for bin and volume
def update_screen(mode, station):
  if mode == "waste":
    show_w()
    show_volume(station["waste"])
  elif mode == "paper":
    show_p()
    show_volume(station["paper"])
  elif mode == "plastics":
    show_l()
    show_volume(station["plastics"])

# Show what bin we are viewing
def show_station_index(index):
  sense.show_letter(str(index), text_colour=red, back_colour=green)

# Read Bin volume information from ThingSpeak
def read_volumes():
  last_levels = reading_saving.get_last_levels()
  bins_list[0]["waste"] = last_levels[0][0]
  bins_list[0]["paper"] = last_levels[0][1]
  bins_list[0]["plastics"] = last_levels[0][2]
  bins_list[1]["waste"] = last_levels[1][0]
  bins_list[1]["paper"] = last_levels[1][1]
  bins_list[1]["plastics"] = last_levels[1][2]
  bins_list[2]["waste"] = last_levels[2][0]
  bins_list[2]["paper"] = last_levels[2][1]
  bins_list[2]["plastics"] = last_levels[2][2]
  
def main():
  # Thingspeak Station IDs
  station0_id=1222563
  station1_id=1222564
  station2_id=1222565

  station_ids = [station0_id, station1_id, station2_id]
  station_index = 0
  num_stations = len(station_ids)

  # Bin types
  bin_index = 0
  bins = ["waste", "paper", "plastics"]
  num_bins = len(bins)
  print("start")

  show_station_index(station_index % num_stations)
  time.sleep(1)
  read_volumes()
  update_screen("waste", bins_list[0])
  update_time = time.perf_counter()
  volume_screen = True

  while True:
    selection = False
    events = sense.stick.get_events()
    for event in events:
      if event.action == "pressed":
        if event.direction == "left":
          bin_index -= 1
          current_mode = bins[bin_index % num_bins]
          update_screen(current_mode, bins_list[station_index % num_stations])
          volume_screen = True
        elif event.direction == "right":
          bin_index += 1
          current_mode = bins[bin_index % num_bins]
          update_screen(current_mode, bins_list[station_index % num_stations])
          volume_screen = True
        elif event.direction == "up":
          station_index += 1
          bin_index = -1
          show_station_index(station_index % num_stations)
          read_volumes()
          volume_screen = False
      elif event.direction == "down":
          station_index -= 1
          bin_index = -1
          show_station_index(station_index % num_stations)
          read_volumes()
          volume_screen = False
      elif event.direction == "middle":
          bin_index = -1
          show_station_index(station_index % num_stations)
          read_volumes()
          volume_screen = False
    if time.perf_counter() - update_time > 30:
      read_volumes()
      if volume_screen:
        current_mode = bins[bin_index % num_bins]
        update_screen(current_mode, bins_list[station_index % num_stations])
      update_time = time.perf_counter()
       
if __name__ == "__main__":
  main()
        
  
  