from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)  # Built-in LED on many ESP32 boards

while True:
    led.on()   # Turn LED on
    sleep(1)
    led.off()  # Turn LED off
    sleep(1)

