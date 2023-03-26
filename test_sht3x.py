from machine import Pin, I2C
from sensor.sht3x import SHT3X

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
sht3x = SHT3X(i2c)


def test():
    print("hello")
    if (sht3x.isConnected()):
        temp, hum, error = sht3x.read()
        if not error:
            print("T: {:.2f}".format(temp))
            print("H: {:.2f}".format(hum))
        else:
            print("CRC error")
    else:
        print("SHT31 not connected")


test()
