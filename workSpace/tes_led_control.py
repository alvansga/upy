from machine import Pin, I2C
import ssd1306
import network
import socket
import time

# === OLED SETUP ===
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# === LED SETUP ===
led = Pin(2, Pin.OUT)

# === WIFI AP SETUP ===
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP32-Hotspot", password="123456789")  # Change password if you want

while not ap.active():
    pass

print("Access Point active")
print("IP:", ap.ifconfig()[0])

# === WEB SERVER SETUP ===
def web_page(led_state):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>ESP32 LED Control</title>
      <style>
        body {{ font-family: Arial; text-align: center; margin-top: 50px; }}
        button {{ font-size: 20px; padding: 15px; margin: 10px; }}
      </style>
    </head>
    <body>
      <h2>ESP32 LED Control</h2>
      <p>LED is currently: <b>{led_state}</b></p>
      <a href="/on"><button style="background:lightgreen;">Turn ON</button></a>
      <a href="/off"><button style="background:lightcoral;">Turn OFF</button></a>
    </body>
    </html>
    """
    return html

# Start socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# === MAIN LOOP ===
while True:
    conn, addr = s.accept()
    print("Client connected from:", addr)
    request = conn.recv(1024).decode()
    print("Request:", request)

    # Default LED state
    led_state = "OFF"

    if "/on" in request:
        led.on()
        led_state = "ON"
    elif "/off" in request:
        led.off()
        led_state = "OFF"

    # Update OLED
    oled.fill(0)
    oled.text("LED " + led_state, 0, 0)
    oled.show()

    # Send response
    response = web_page(led_state)
    conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    conn.send(response)
    conn.close()

