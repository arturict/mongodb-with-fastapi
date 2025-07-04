from machine import Pin
from utime import sleep
import network
import urequests
import ujson
import time
import ubinascii
import ujson
import dht
 
pin =Pin("LED", Pin.OUT)
pwrPin = Pin(0, Pin.OUT)
pwrPin.on()
 
sensor = dht.DHT11(Pin(1))
 
print("LED starts flashing...")
while True:
    try:
        pin.toggle()
        sleep(1)
        sensor.measure()
        temperature = sensor.temperature() #Sensor gets temperatur value as an object, we need to convert to JSON String
        humdity = sensor.humidity()
        print("Humidity: {} %".format(humdity))
        print("Temperature: {} C".format(temperature))
    except KeyboardInterrupt:
        print("Exiting...")
        break
    
#WLAN-Daten
ssid = "pico-wifi-77"
password = "pico-pw-69"

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