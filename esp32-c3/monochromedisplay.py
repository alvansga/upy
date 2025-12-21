
import ssd1306
from machine import Pin, I2C

# OLED setup
i2c = I2C(0, scl=Pin(6), sda=Pin(7)) # esp32-c3
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def goToLightSleep():
    import machine
    print("Go to light sleep...")
    machine.lightsleep()  # 1 minute

def updateScreen():
    filename = "oled_image.bin"

    try:
        with open(filename, "rb") as f:
            for page in range(8):  # 8 pages
                for x in range(128):
                    byte = f.read(1)
                    if not byte:
                        print("Image too small")
                        return
                    b = byte[0]
                    for bit in range(8):
                        color = (b >> bit) & 1
                        oled.pixel(x, page * 8 + bit, color)

        oled.invert(True)
        oled.show()

    except Exception as e:
        print("Error loading image:", e)
updateScreen()

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
    while True:
        data = conn.recv(1024)
        if not data:
            print("Client disconnected.")
            break
        
        # 🧠 Binary mode
        filename = "oled_image.bin"
        print("Receiving binary file...")
        with open(filename, "wb") as f:
            total_bytes = 0

            # write the first data chunk too!
            f.write(data)
            total_bytes += len(data)

            # continue reading remaining bytes
            while True:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
                total_bytes += len(chunk)

        print(f"Received {total_bytes} bytes total.")
        conn.send(b"File received successfully!\n")

except Exception as e:
    print("Error:", e)

finally:
    conn.close()
    server.close()
    print("Server closed.")
    
updateScreen()
goToLightSleep()




