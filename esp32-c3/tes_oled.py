from machine import I2C, Pin
import ssd1306

i2c = I2C(0, scl=Pin(9), sda=Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.text("Hello", 0, 0)
oled.show()
