# [z] class tft_display.py

from ST7735 import TFT,TFTColor
from machine import SPI,Pin

class TftDisplay:

    def __init__(self, 
                 sck_pin=6, 
                 mosi_pin=7, 
                 bl_pin=3, 
                 dc_pin=4, 
                 cs_pin=5, 
                 rst_pin=2):
        # TFT setup
        try:
            self.spi = SPI(
                1,
                baudrate=20_000_000,
                polarity=0,
                phase=0,
                sck= Pin( sck_pin ),
                mosi= Pin( mosi_pin ),
                miso=None
            )

            self.tft = TFT(
                self.spi,
                dc_pin,
                rst_pin,
                cs_pin
            )

            self.bl = Pin(bl_pin, Pin.OUT)
            self.bl.on()   # WAJIB HIGH

            self.tft.initr()
            self.tft.rgb(True)
            # self.tft.fill(TFT.BLACK)

        except Exception as e:
            print("Error initializing TFT:", e)
            self.spi = None
            self.tft = None
            self.bl = None

    def updateScreen(self, filename='image_24bit.bmp'):
        try:
            f=open(filename, 'rb')
            if f.read(2) == b'BM':  #header
                dummy = f.read(8) #file size(4), creator bytes(4)
                offset = int.from_bytes(f.read(4), 'little')
                hdrsize = int.from_bytes(f.read(4), 'little')
                width = int.from_bytes(f.read(4), 'little')
                height = int.from_bytes(f.read(4), 'little')
                if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
                    depth = int.from_bytes(f.read(2), 'little')
                    if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
                        print("Image size:", width, "x", height)
                        rowsize = (width * 3 + 3) & ~3
                        if height < 0:
                            height = -height
                            flip = False
                        else:
                            flip = True
                        w, h = width, height
                        if w > 128: w = 128
                        if h > 160: h = 160
                        self.tft._setwindowloc((0,0),(w - 1,h - 1))
                        for row in range(h):
                            if flip:
                                pos = offset + (height - 1 - row) * rowsize
                            else:
                                pos = offset + row * rowsize
                            if f.tell() != pos:
                                dummy = f.seek(pos)
                            for col in range(w):
                                bgr = f.read(3)
                                self.tft._pushcolor(TFTColor(bgr[2],bgr[1],bgr[0]))

        except Exception as e:
            print("Error loading image:", e)
        
        print("TFT updateScreen done.")