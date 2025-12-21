# [z] class oled_display.py

import ssd1306
from machine import Pin, I2C

class OledDisplay:

    def __init__(self, scl_pin=6, sda_pin=7, width=128, height=64):
        # OLED setup
        try:
            self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin)) # esp32-c3
            self.oled = ssd1306.SSD1306_I2C(width, height, self.i2c)
        except Exception as e:
            print("Error initializing OLED:", e)

    def updateScreen(self, filename="oled_image.bin"):
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
                            self.oled.pixel(x, page * 8 + bit, color)

            self.oled.invert(True)
            self.oled.show()

        except Exception as e:
            print("Error loading image:", e)