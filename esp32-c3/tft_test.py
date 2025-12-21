from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin
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

tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

tft.text((0, 0), "ESP32-C3 OK", TFT.WHITE, sysfont )
time.sleep(2)
