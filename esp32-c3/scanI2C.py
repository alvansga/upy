from machine import Pin, I2C

# ganti kombinasi pin dan tes sampai ketemu address
for sda, scl in [(6,7), (8,9), (4,5)]:
    print("Testing SDA=", sda, "SCL=", scl)
    try:
        i2c = I2C(0, scl=Pin(scl), sda=Pin(sda))
        devices = i2c.scan()
        if devices:
            print("Found I2C devices at:", [hex(d) for d in devices])
        else:
            print("No device found.")
    except Exception as e:
        print("Error:", e)
