from PIL import Image, ImageEnhance
import numpy as np

img = Image.open("chopper.jpg")
img = img.rotate(90, expand=True)
img = img.resize((128, 64))
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2.0)
sharpener = ImageEnhance.Sharpness(img)
img = sharpener.enhance(2.0)
img = img.convert("1").resize((128, 64))
img.save("oled_image_out.bmp")

pixels = np.array(img)

height, width = pixels.shape
buffer = bytearray(width * height // 8)

for y in range(height):
    for x in range(width):
        if pixels[y, x] == 0:  # black pixel
            buffer[x + (y // 8) * width] |= (1 << (y % 8))

with open("oled_image.bin", "wb") as f:
    f.write(buffer)
