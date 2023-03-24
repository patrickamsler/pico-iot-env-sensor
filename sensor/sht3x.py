from machine import Pin, I2C
from sensor.crc_calculator import CrcCalculator


class Sht3x:
    sht3xI2cAddr = 0x45
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
    crc8 = CrcCalculator(8, 0x31)

    def isConnected(self):
        response = self.i2c.scan()
        return self.sht3xI2cAddr in response

    def readData(self):
        # single shot measurement with clock stretching enabled
        self.i2c.writeto(self.sht3xI2cAddr, b'\x2c\x06')

        # readout of single shot measurement (8 bytes) after sensor acknowledge
        data = self.i2c.readfrom(self.sht3xI2cAddr, 8)

        temp = (data[0] << 8) + data[1]
        humidity = (data[3] << 8) + data[4]

        print(data[3])
        print(self.crc8([data[0], data[1]]))

        tempCelsius = ((175.72 * temp) / 65536.0) - 45
        humidityRelative = ((100 * humidity) / 65536.0)

        return tempCelsius, humidityRelative
