from machine import SPI, Pin
from ST7735 import TFT
import time

spi = SPI(
    1,
    baudrate=20_000_000,
    polarity=0,
    phase=0,
    sck=Pin(6),
    mosi=Pin(7),
    miso=None
)

tft = TFT(
    spi,
    4,
    2,
    5
)

bl = Pin(3, Pin.OUT)
bl(1)   # WAJIB HIGH

colors = [
    TFT.RED,
    TFT.GREEN,
    TFT.BLUE,
    TFT.WHITE,
]



tft.initr()      # init display
tft.rgb(False)    # RGB order
tft.fill(TFT.RED)
print("white done")
while True:
    for c in colors:
        tft.fill(c)
        time.sleep(1)
        print("1s")
