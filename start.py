from config import load_config
from wireless.wifi import Wifi
from sensor.sht3x import SHT3X
from umqtt.simple import MQTTClient
from machine import Pin, I2C, Timer
import time


def main():
    config = load_config()

    # initialize sensor
    sht31 = SHT3X(
        i2c=I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
    )
    if not sht31.isConnected():
        raise RuntimeError("SHT31 not found on I2C bus")

    # connect to WiFi
    wifi = Wifi(
        ssid=config['wlan.ssid'],
        password=config['wlan.password']
    )
    wifi.connect()

    # initialize mqtt client
    mqtt_temperature_topic = config["mqtt.topics.temperature"]
    mqtt_humidity_topic = config["mqtt.topics.humidity"]
    mqtt_client = MQTTClient(
        client_id=config["mqtt.clientId"],
        server=config['mqtt.broker'],
        user=config['mqtt.user'],
        password=config['mqtt.password']
    )

    # main data acquisition an publishing loop
    def publish_data(timer):
        if not wifi.is_connected():
            print("WiFi not connected. Not publishing data")
            return

        temp, hum, error = sht31.read()
        if error:
            print("Error reading sensor. Not publishing data")
            return

        if not error:
            print("Publishing data...", "Temperature: " + str(temp) + "°C", "Humidity: " + str(hum) + "%")
            try:
                mqtt_client.connect()
                mqtt_client.publish(mqtt_temperature_topic, str(temp), retain=False, qos=0)
                mqtt_client.publish(mqtt_humidity_topic, str(hum), retain=False, qos=0)
                mqtt_client.disconnect()
                print("Data published successfully")
            except Exception as e:
                print("Error publishing data:", e)


    # start the timer for the main loop
    timer = Timer()
    timer.init(period=20000, mode=Timer.PERIODIC, callback=publish_data)

# start the main function
if __name__ == "__main__":
    main()
