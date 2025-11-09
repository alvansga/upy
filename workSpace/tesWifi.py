import network
import time

ssid = "alvaa"
password = "88888888"

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

print("Connecting to WiFi...", end="")
while not wifi.isconnected():
    print(".", end="")
    time.sleep(0.5)

print("\nConnected!")
print("IP address:", wifi.ifconfig()[0])


import socket

host = "10.150.228.93"  # Replace with your server IP
port = 5000             # Replace with your server port

print(f"Connecting to TCP server {host}:{port}...")
s = socket.socket()
try:
    s.connect((host, port))
    print("Connected to server!")

    # Send data
    s.send(b"Hello from ESP32!\n")

    # Receive response
    data = s.recv(1024)
    print("Received from server:", data.decode())

except Exception as e:
    print("Connection failed:", e)
finally:
    s.close()
    print("Socket closed.")

