import http.client
import urllib.parse
from time import sleep

key_WS_1 = "BLT9N7F99578BAAM"
key_WS_2 = "GDHEA7VGR18FXYSU"  
key_WS_3 = "KBQ5HYT7A32U1TQK" 

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
    update_levels(key_WS_1, 0, 0, 0)
    update_levels(key_WS_2, 0, 0, 0)
    update_levels(key_WS_3, 0, 0, 0)
    sleep(5)
    update_levels(key_WS_1, 20, 30, 15)
    sleep(5)
    update_levels(key_WS_2, 50, 60, 20)
    sleep(5)
    update_levels(key_WS_3, 40, 55, 10)
    sleep(5)
    update_levels(key_WS_3, 65, 70, 35)
    sleep(5)
    update_levels(key_WS_3, 70, 90, 50)
    sleep(5)
    update_levels(key_WS_2, 50, 60, 35)
    sleep(5)
    update_levels(key_WS_3, 95, 50, 60)
    
    