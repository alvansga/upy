from machine import Pin, I2C
import ssd1306, framebuf

# OLED init
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Load binary image
with open("oled_image.bin", "rb") as f:
    buffer = f.read()

# Create framebuffer from buffer
fb = framebuf.FrameBuffer(bytearray(buffer), 128, 64, framebuf.MONO_VLSB)

# Blit framebuffer onto OLED
oled.blit(fb, 0, 0)
oled.show()
