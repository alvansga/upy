# OLED setup
from oled_display import OledDisplay
#from tft_display import TftDisplay


oled_display = OledDisplay()
oled_display.updateScreen("oled_image.bin")

# tft_display = TftDisplay()
# tft_display.updateScreen("image_24bit.bmp")


def goToLightSleep():
    import machine
    print("Go to light sleep...")
    machine.lightsleep()  # 1 minute

import network
import socket
import time

# Access Point credentials
AP_SSID = "ESP32_AP"
AP_PASSWORD = "12345678"

# Create access point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD, authmode=network.AUTH_WPA_WPA2_PSK)

print("Starting Access Point...")
while not ap.active():
    time.sleep(0.5)

print("Access Point active!")
print("AP IP address:", ap.ifconfig()[0])

# TCP server setup
PORT = 5000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ap.ifconfig()[0], PORT))
server.listen(1)
server.settimeout(120)  # 3 minutes = 180 seconds
print(f"TCP Server listening on {ap.ifconfig()[0]}:{PORT}. You have 2 minutes to connect!")

try:
    conn, addr = server.accept()
    print("Client connected from:", addr)
except Exception as e:
    print("no client connected:", str(e))
    goToLightSleep()

try:
    filename = "oled_image.bin"
    total = 0

    with open(filename, "wb") as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
            total += len(data)

    print("Saved", total, "bytes")

except Exception as e:
    print("Error:", e)

finally:
    conn.close()
    server.close()
    ap.active(False)
    print("Server closed.")
    
oled_display.updateScreen()
# tft_display.updateScreen()
goToLightSleep()






