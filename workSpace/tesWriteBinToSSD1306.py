
import ssd1306
from machine import Pin, I2C

# OLED setup
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Load image buffer
with open("shella.bin", "rb") as f:
    buffer = f.read()

# Show image
#oled.blit_framebuffer(buffer, 0, 0)  # if your SSD1306 lib supports blit
for page in range(8):  # 8 pages = 64 pixels / 8
    for x in range(128):
        byte = buffer[page * 128 + x]
        for bit in range(8):
            color = (byte >> bit) & 1
            oled.pixel(x, page * 8 + bit, color)
            
oled.invert(True)
oled.show()


