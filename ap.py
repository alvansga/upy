try:
    import usocket as socket
except:
    import socket

import network

import esp
esp.osdebug(None)

import gc
gc.collect()

from time import sleep

ssid = "esp32"
pw = "qqqqwwww"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=pw)

print(f"Connecting to {ssid}, please wait.",end="")
while ap.active() == False:
    print(".")
    sleep(0.5)
print("\nConnected successful!")

def web_page():
    html = '''<html>
    <body><h1>Hello world</h1></body></html>'''
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80 ))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    req = conn.recv(1024)
    print("Content = %s" % str(req))
    response = web_page()
    conn.send(response)
    conn.close()