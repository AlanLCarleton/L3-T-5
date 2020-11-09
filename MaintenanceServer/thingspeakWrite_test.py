import http.client
import urllib.parse
import time

key_WS_1 = "BLT9N7F99578BAAM"
def update_levels(channel_key, level1, level2, level3):
    while True:
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
        break
if __name__ == "__main__":
    while True:
        update_levels(key_WS_1, 1.1, 2.2, 3.3)