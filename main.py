from sensor.sht3x import Sht3x
# from machine import Timer

# timer = Timer()

sht3x = Sht3x()

def test():
    print("hello")
    if (sht3x.isConnected()):
        temp, hum, error = sht3x.readData()
        if not error:
            print("T: {:.2f}".format(temp))
            print("H: {:.2f}".format(hum))
        else:
            print("CRC error")
    else:
        print("SHT31 not connected")


test()

# timer.init(freq=0.5, mode=Timer.PERIODIC, callback=test)
