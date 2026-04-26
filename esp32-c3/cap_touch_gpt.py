from machine import Pin
import time

class CapacitiveTouch:
    def __init__(self, pin_num, active_high=True, debounce_ms=50):
        self.pin = Pin(pin_num, Pin.IN)
        self.active_high = active_high
        self.debounce_ms = debounce_ms

        self._last_state = self.raw_value()
        self._stable_state = self._last_state
        self._last_change_time = time.ticks_ms()

    def raw_value(self):
        val = self.pin.value()
        return val if self.active_high else not val

    def update(self):
        now = time.ticks_ms()
        current = self.raw_value()

        if current != self._last_state:
            self._last_change_time = now
            self._last_state = current

        if time.ticks_diff(now, self._last_change_time) > self.debounce_ms:
            if self._stable_state != current:
                self._stable_state = current
                return True  # state changed

        return False

    def is_pressed(self):
        return self._stable_state
    

if __name__ == "__main__":
    touch = CapacitiveTouch(pin_num=1)
    
    while True:
        if touch.update():
            if touch.is_pressed():
                print("TOUCHED")
            else:
                print("RELEASED")