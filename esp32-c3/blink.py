from machine import Pin
import time

led = Pin(8, Pin.OUT)  # Try 8 first

while True:
    led.off()
    time.sleep(0.1)
    led.on()
    time.sleep(0.1)

    led.off()
    time.sleep(0.1)
    led.on()
    time.sleep(0.7)