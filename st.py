from time import sleep
import network 

# setting up station network ---------

sta_if = network.WLAN(network.STA_IF)

ssid = "your_ssid_here"
pw = "your_password_here"

def connect(sta_if):
    try:
        sta_if.active(True)
        sta_if.connect( ssid, pw )
    except OSError:
        #wifi internal error
        return

    print(f"Connecting to {ssid}. Please wait.",end="")
    while not sta_if.isconnected():
        print(".")
        sleep(0.5)

    print("\nConnected successful!")

    def printMyIp(sta_if):
        ip, mask = sta_if.ipconfig("addr4")
        print(f"My Ip Info: {ip} ,mask: {mask}")

    printMyIp(sta_if)

connect(sta_if)
# setting up station network finished ---------

def start_starwars_asciimation():
    import socket

    addr_info = socket.getaddrinfo("towel.blinkenlights.nl",23)
    addr = addr_info[0][-1]

    s = socket.socket()
    s.connect(addr)

    while True:
        data = s.recv(1024)
        print(str(data, "utf8"), end="")

while True:
    try:
        start_starwars_asciimation()
    except OSError:
        # when disconnected try to connect again
        sleep(3)
        connect(sta_if)