# ===== OLED SETUP =====
from oled_display import OledDisplay
from machine import Pin
import os
import network
import socket
import time

# ===== TOUCH CLASS (ringkas dari sebelumnya) =====
class CapacitiveTouch:
    def __init__(self, pin_num, active_high=True, debounce_ms=50):
        self.pin = Pin(pin_num, Pin.IN)
        self.active_high = active_high
        self.debounce_ms = debounce_ms

        self._last = self._read()
        self._stable = self._last
        self._last_time = time.ticks_ms()

    def _read(self):
        val = self.pin.value()
        return val if self.active_high else not val

    def update(self):
        now = time.ticks_ms()
        cur = self._read()

        if cur != self._last:
            self._last = cur
            self._last_time = now

        if time.ticks_diff(now, self._last_time) > self.debounce_ms:
            if self._stable != cur:
                self._stable = cur
                return True
        return False

    def is_pressed(self):
        return self._stable


# ===== FILE MANAGER =====
DIR = "oled_image"

def ensure_dir():
    try:
        os.mkdir(DIR)
    except:
        pass

def list_bins():
    files = os.listdir(DIR)
    bins = [f for f in files if f.endswith(".bin")]
    bins.sort(key=lambda x: int(x.replace(".bin", "")))
    return bins

def next_filename():
    bins = list_bins()
    if not bins:
        return "0.bin"
    last = int(bins[-1].replace(".bin", ""))
    return f"{last + 1}.bin"


# ===== OLED =====
oled = OledDisplay()

# ===== INIT DIR & LOAD FIRST IMAGE =====
ensure_dir()
bin_list = list_bins()
current_index = 0

if bin_list:
    oled.updateScreen(f"{DIR}/{bin_list[0]}")
else:
    print("No images yet.")

# ===== TOUCH INIT =====
touch = CapacitiveTouch(pin_num=1)

# ===== WIFI AP =====
AP_SSID = "ESP32_AP"
AP_PASSWORD = "12345678"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD, authmode=network.AUTH_WPA_WPA2_PSK)

while not ap.active():
    time.sleep(0.5)

ip = ap.ifconfig()[0]
print("AP IP:", ip)

# ===== TCP SERVER =====
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, 5000))
server.listen(1)
server.setblocking(False)

print("Server ready...")

# ===== MAIN LOOP =====
while True:

    # --- HANDLE TOUCH ---
    if touch.update() and touch.is_pressed():
        bin_list = list_bins()
        if bin_list:
            current_index = (current_index + 1) % len(bin_list)
            file_path = f"{DIR}/{bin_list[current_index]}"
            print("Show:", file_path)
            oled.updateScreen(file_path)

    # --- HANDLE TCP ---
    try:
        conn, addr = server.accept()
        print("Client:", addr)

        filename = next_filename()
        filepath = f"{DIR}/{filename}"

        total = 0
        with open(filepath, "wb") as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)
                total += len(data)

        print("Saved:", filepath, total, "bytes")

        conn.close()

        # refresh list setelah nambah file
        bin_list = list_bins()

    except:
        pass  # non-blocking, jadi ya sering gagal, santai aja

    time.sleep_ms(10)