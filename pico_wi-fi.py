import network
import urequests
import ujson
import time
import ubinascii
import ujson

#WLAN-Daten
ssid = "corredtSSID"
password = "passw"

#WLAN verbinden
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
 
while not wlan.isconnected():
    print('Waiting for connection...')
    time.sleep(1)
print("Connected:", wlan.ifconfig())

#Todo Wlan einstellen, damit man darauf zugreifen kann (bzw. Daten bekommen)

#Function to fetch data from a URL

def fetch_data(url):
    try:
        response = urequests.get(url)
        print("Status:", response.status_code)
        print("Data:", response.text)
        temperature = response.text
        response.close()
        return temperature
    except Exception as e:
        print("Error fetching data:", e)
        return None



temperature = urequests.get.text
toJson = ujson.dumps(temperature)
