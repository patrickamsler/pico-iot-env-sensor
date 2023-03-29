from network import WLAN, STA_IF

class Wifi:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = WLAN(STA_IF)

    def connect(self):
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        self.wait_for_connection()
    
    def is_connected(self):
        return self.wlan.isconnected()
    
    def wait_for_connection(self):
        print("waiting for wifi connection ...")
        while not self.is_connected():
            pass
        status = self.wlan.ifconfig()
        print("connected to WiFi network: ", status)
    