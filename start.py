from util.config import load_config
from wireless.wifi import Wifi
from sensor.sht3x import SHT3X
from umqtt.simple import MQTTClient
from machine import Pin, I2C, Timer
import util.logging as logging
import sys

def init_logging():
    # logging.basicConfig(filename='log-file.log', level=logging.DEBUG, filemode='a') # log to file
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout) # log to console
    for handler in logging.getLogger().handlers:
        handler.setFormatter(logging.Formatter("[%(levelname)s] - %(name)s - %(message)s"))

def main():
    init_logging()
    log = logging.getLogger(__name__)
    config = load_config()

    log.info("initializing SHT31 sensor")
    sht31 = SHT3X(
        i2c=I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
    )
    if not sht31.isConnected():
        raise RuntimeError("SHT31 not found on I2C bus")

    log.info("initializing WiFi")
    wifi = Wifi(
        ssid=config['wlan.ssid'],
        password=config['wlan.password']
    )
    wifi.connect()

    log.info("initializing MQTT client")
    mqtt_temperature_topic = config["mqtt.topics.status"]
    mqtt_clientId = config["mqtt.clientId"]
    mqtt_client = MQTTClient(
        client_id=mqtt_clientId,
        server=config['mqtt.broker'],
        user=config['mqtt.user'],
        password=config['mqtt.password']
    )

    # main data acquisition an publishing loop
    def publish_data(timer):
        if not wifi.is_connected():
            log.info("WiFi not connected. Not publishing data")
            return

        temp, hum, error = sht31.read()
        if error:
            log.error("Error reading sensor data")
            return

        payload = {
            "temperature": temp,
            "humidity": hum,
            "clientId": mqtt_clientId
        }

        if not error:
            log.debug("Publishing data: " + str(payload))
            try:
                mqtt_client.connect()
                mqtt_client.publish(mqtt_temperature_topic, str(payload), retain=False, qos=0)
                mqtt_client.disconnect()
                log.debug("Data published")
            except Exception as e:
                log.error("Error publishing data: ", e)

    log.info("starting data acquisition loop")
    timer = Timer()
    timer.init(period=20000, mode=Timer.PERIODIC, callback=publish_data)


# start the main function
if __name__ == "__main__":
    main()
