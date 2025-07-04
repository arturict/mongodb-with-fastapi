from machine import Pin
from utime import sleep
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
        temperature = sensor.temperature()
        print("Temperature: {} C".format(temperature))
    except KeyboardInterrupt:
        print("Exiting...")
        break