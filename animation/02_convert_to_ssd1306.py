import cv2
import numpy as np
import os

WIDTH = 128
HEIGHT = 64

def convert_to_ssd1306_buffer(img):
    # threshold
    THRESH = 150  # coba 60–120, tergantung gambar

    _, bw = cv2.threshold(img, THRESH, 1, cv2.THRESH_BINARY)
    # _, bw = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)

    buffer = bytearray(WIDTH * HEIGHT // 8)

    for x in range(WIDTH):
        for y in range(HEIGHT):
            if bw[y][x]:
                byte_index = x + (y // 8) * WIDTH
                bit = y % 8
                buffer[byte_index] |= (1 << bit)

    return buffer


for file in sorted(os.listdir("frames")):
    img = cv2.imread("frames/" + file, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (WIDTH, HEIGHT))

    buf = convert_to_ssd1306_buffer(img)

    with open(f"out/{file}.bin", "wb") as f:
        f.write(buf)