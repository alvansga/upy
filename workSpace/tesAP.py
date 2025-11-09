import network
import socket
import time

# Access Point credentials
AP_SSID = "ESP32_AP"
AP_PASSWORD = "12345678"

# Create access point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD)

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
print(f"TCP Server listening on {ap.ifconfig()[0]}:{PORT}")

conn, addr = server.accept()
print("Client connected from:", addr)

try:
    while True:
        data = conn.recv(1024)
        if not data:
            print("Client disconnected.")
            break
        
        msg = data.decode().strip()
        print("Received:", msg)
         
        
        if (msg == "hi"):
            print("send back: hi")
            conn.send(b"hi! :)")
        else:
            pass
        # Send a reply
        #conn.send(b"ACK from ESP32 AP server\n")

except Exception as e:
    print("Error:", e)

finally:
    conn.close()
    server.close()
    print("Server closed.")

