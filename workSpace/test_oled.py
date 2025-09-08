from machine import Pin, I2C
from time import sleep
import ssd1306

# I2C setup (GPIO 22 = SCL, GPIO 21 = SDA)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Create OLED object
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display
oled.fill(0)
oled.text("Hello from ESP32!", 0, 0)
oled.show()

# Built-in LED on GPIO 2
led = Pin(2, Pin.OUT)

# Blink LED with OLED message
while True:
    led.on()
    oled.fill(0)
    oled.text("LED ON", 0, 0)
    oled.show()
    sleep(1)
    
    led.off()
    oled.fill(0)
    oled.text("LED OFF", 0, 0)
    oled.show()
    sleep(1)

