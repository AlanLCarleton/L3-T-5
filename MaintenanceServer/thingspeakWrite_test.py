import http.client
import urllib.parse
import time

key = "BLT9N7F99578BAAM" # Put your API Key here
def thermometer():
    while True:
    #Calculate CPU temperature of Raspberry Pi in Degrees C
        temp = 5
        params = urllib.parse.urlencode({'field1': temp, 'key':key })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers) 
            response = conn.getresponse()
            print(temp)
            print(response.status, response.reason)
            data = response.read()
            conn.close()
        except:
            print("connection failed")
        break
if __name__ == "__main__":
    while True:
        thermometer()