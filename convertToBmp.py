from PIL import Image
from PIL import ImageEnhance


# Load your image
img = Image.open("chopper.jpg")
img = img.resize((128, 64))

enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2.0)
sharpener = ImageEnhance.Sharpness(img)
img = sharpener.enhance(2.0)

img = img.convert("1", dither=Image.FLOYDSTEINBERG)

# Save as raw monochrome bitmap
img.save("oled_image.bmp")
