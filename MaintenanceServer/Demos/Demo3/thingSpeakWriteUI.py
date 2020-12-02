import http.client
import urllib.parse
from time import sleep

key_WS_0 = "BLT9N7F99578BAAM"
key_WS_1 = "GDHEA7VGR18FXYSU"  
key_WS_2 = "KBQ5HYT7A32U1TQK" 

def update_levels(channel_key, level1, level2, level3):
    params = urllib.parse.urlencode({'field2': level1,'field3': level2,'field4': level3,'key':channel_key })
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers) 
        response = conn.getresponse()
        print(response.status, response.reason)
        conn.close()
    except:
        print("connection failed")
       
if __name__ == "__main__":
    while(True):
        stationID = int(input("Choose between station 0, 1 or 2."))
        if not (0 <= stationID <= 2):
            continue
        waste_volume = int(input("Select waste volume in percentage."))
        if not (0 <= waste_volume <= 100):
            print("Invalid waste percentage provided")
            continue
        paper_volume = int(input("Select paper volume in percentage."))
        if not (0 <= paper_volume <= 100):
            print("Invalid paper percentage provided")
            continue
        plastics_volume = int(input("Select plastics volume in percentage."))
        if not (0 <= plastics_volume <= 100):
            print("Invalid plastics percentage provided")
            continue
        if stationID == 0:
            update_levels(key_WS_0, waste_volume, paper_volume, plastics_volume)
        elif stationID == 1:
            update_levels(key_WS_1, waste_volume, paper_volume, plastics_volume)
        elif stationID == 2:
            update_levels(key_WS_2, waste_volume, paper_volume, plastics_volume)
    
    
