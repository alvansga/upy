from oled_display import OledDisplay
from cap_touch_gpt import CapacitiveTouch
from time import sleep_ms

# ===== TOUCH INIT =====
touch = CapacitiveTouch(pin_num=1)

# ===== OLED INIT =====
oled_display = OledDisplay()
oled_display.playAnimation("anim.bin")

# ===== MAIN LOOP =====
while True:

    # --- HANDLE TOUCH ---
    if touch.update() and touch.is_pressed():
        oled_display.playAnimation("anim.bin")

    sleep_ms(10)