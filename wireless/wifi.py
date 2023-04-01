from network import WLAN, STA_IF
import util.logging as logging

log = logging.getLogger(__name__)


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
        log.info("waiting for wifi connection ...")
        while not self.is_connected():
            pass
        status = self.wlan.ifconfig()
        log.debug("connected to WiFi network: " + str(status))
