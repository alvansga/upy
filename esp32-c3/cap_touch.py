from machine import Pin
import time
import thread

class CapTouchSensor():
    self._value = False
    
    def __init__(self, pin_cap):
        self.pin_cap = pin_cap
        self.touch = Pin(self.pin_cap, Pin.IN)
    
    def loop(self):
        while True:
            if self._value == False:
                if touch.value():
                    self._value = True
                
    
touch = Pin(1, Pin.IN)
while True:
    print(touch.value())
    time.sleep(0.2)
