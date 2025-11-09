import network
import socket
import time
import os

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
ip = ap.ifconfig()[0]
print("AP IP address:", ip)

# TCP server setup
PORT = 5000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, PORT))
server.listen(1)
print(f"TCP Server listening on {ip}:{PORT}")

conn, addr = server.accept()
print("Client connected from:", addr)

# File to store incoming binary
filename = "oled_image.bin"
try:
    with open(filename, "wb") as f:
        total_bytes = 0
        while True:
            data = conn.recv(1024)
            if not data:
                print("Client disconnected.")
                break
            f.write(data)
            total_bytes += len(data)
        print(f"Received {total_bytes} bytes total.")
        conn.send(b"File received successfully!\n")

except Exception as e:
    print("Error:", e)

finally:
    conn.close()
    server.close()
    print("Server closed.")

