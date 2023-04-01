from machine import I2C

SHT3X_IC2_ADDR_A = 0x44 # used by sht31 from M5 Stack
SHT3X_IC2_ADDR_B = 0x45 # used by sht35 from Grove

class SHT3X:

    def __init__(self, i2c: I2C, addr=SHT3X_IC2_ADDR_A):
        self.i2c = i2c
        self.addr = addr

    def isConnected(self):
        response = self.i2c.scan()
        return self.addr in response

    def read(self):
        # single shot measurement with clock stretching enabled
        self.i2c.writeto(self.addr, b'\x2c\x06')

        # readout of single shot measurement (8 bytes) after sensor acknowledge
        data = self.i2c.readfrom(self.addr, 8)

        # convert 16bit data
        temp = (data[0] << 8) + data[1]
        tempCrc = data[2]
        humidity = (data[3] << 8) + data[4]
        humidityCrc = data[5]

        # checksum
        error = self.crc8(data[0:2]) != tempCrc or self.crc8(data[3:5]) != humidityCrc

        tempCelsius = ((175.72 * temp) / 65536.0) - 45
        humidityRelative = ((100 * humidity) / 65536.0)

        return tempCelsius, humidityRelative, error

    def crc8(self, data):
        polynomial = 0x31
        crc = 0xFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc <<= 1
        return crc & 0xFF
