import http.client
import urllib.parse
import time

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
    update_levels(key_WS_3, 7, 8, 9)