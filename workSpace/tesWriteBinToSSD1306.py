import ssd1306
from machine import Pin, I2C

# OLED setup
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Load image buffer
with open("oled_image.bin", "rb") as f:
    buffer = f.read()

# Show image
oled.blit_framebuffer(buffer, 0, 0)  # if your SSD1306 lib supports blit
oled.show()
