from network import WLAN, STA_IF, STAT_IDLE, STAT_CONNECTING, STAT_WRONG_PASSWORD, STAT_NO_AP_FOUND, STAT_CONNECT_FAIL, STAT_GOT_IP
import util.logging as logging
import time

log = logging.getLogger(__name__)


class Wifi:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = WLAN(STA_IF)

    def connect(self, timeout=-1):
        start_time = time.time()
        # we try to connect to the WiFi network with the given timeout
        # if the timeout is negative, we try forever
        while True:
            self.wlan.active(True)
            self.wlan.connect(self.ssid, self.password)
            try:
                self.wait_for_connection()
                return
            except Exception as e:
                log.error(str(e))
                # check if we have a timeout and raise an exception if we reached it
                if timeout > 0 and time.time() - start_time > timeout:
                    raise Exception("WiFi connection timed out")
                log.debug("retry in 5 seconds")
                time.sleep(5)

    def is_connected(self):
        return self.wlan.isconnected()

    def wait_for_connection(self):
        log.info("waiting for wifi connection ...")
        self.log_status()

        # we wait for the connection to be established
        # if the connection fails, we raise an exception
        while not self.is_connected():
            if (self.wlan.status() < 0):
                self.log_status()
                raise Exception("Connecting to WiFi failed")

        # log the connection status
        ifconfig = self.wlan.ifconfig()
        log.debug("connected to WiFi network: " + str(ifconfig))

    def log_status(self):
        status = self.wlan.status()
        if (status == STAT_IDLE):
            log.debug("WiFi status: STAT_IDLE - no connection and no activity")
        elif (status == STAT_CONNECTING):
            log.debug("WiFi status: STAT_CONNECTING - connecting in progress")
        elif (status == STAT_WRONG_PASSWORD):
            log.debug("WiFi status: STAT_WRONG_PASSWORD - failed due to incorrect password")
        elif (status == STAT_NO_AP_FOUND):
            log.debug("WiFi status: STAT_NO_AP_FOUND - failed because no access point replied")
        elif (status == STAT_CONNECT_FAIL):
            log.debug("WiFi status: STAT_CONNECT_FAIL - failed due to other problems")
        elif (status == STAT_GOT_IP):
            log.debug("WiFi status: STAT_GOT_IP - connection successful")
        else:
            log.debug("WiFi status: unknown")
