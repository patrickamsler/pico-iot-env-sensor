from sensor.crc_calculator import CrcCalculator
from machine import I2C


class SHT3X:
    SHT3X_IC2_ADDR = 0x45
    crc8 = CrcCalculator(width=8,
                         polynomial=0x31,
                         init_value=0xFF,
                         final_xor=0x00)

    def __init__(self, i2c: I2C):
        self.i2c = i2c

    def isConnected(self):
        response = self.i2c.scan()
        return self.SHT3X_IC2_ADDR in response

    def readData(self):
        # single shot measurement with clock stretching enabled
        self.i2c.writeto(self.SHT3X_IC2_ADDR, b'\x2c\x06')

        # readout of single shot measurement (8 bytes) after sensor acknowledge
        data = self.i2c.readfrom(self.SHT3X_IC2_ADDR, 8)

        # convert 16bit data
        temp = (data[0] << 8) + data[1]
        tempCrc = data[2]
        humidity = (data[3] << 8) + data[4]
        humidityCrc = data[5]

        # checksum
        error = self.crc8(data[0:2]) != tempCrc or self.crc8(
            data[3:5]) != humidityCrc

        tempCelsius = ((175.72 * temp) / 65536.0) - 45
        humidityRelative = ((100 * humidity) / 65536.0)

        return tempCelsius, humidityRelative, error
