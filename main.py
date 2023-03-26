from config import load_config
from wireless.wifi import Wifi
from sensor.sht3x import SHT3X
from umqtt.simple import MQTTClient
from machine import Pin, I2C, Timer
import time

def main():
    config = load_config()

    # connect to WiFi
    wifi = Wifi(
        ssid=config['wlan.ssid'],
        password=config['wlan.password']
    )
    wifi.wait_for_connection()

    # initialize sensor
    sht31 = SHT3X(
        i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
    )
    if not sht31.isConnected():
        raise RuntimeError("SHT31 not found on I2C bus")

    # initialize mqtt client
    mqtt_temperature_topic = "livingroom/temperature" #TODO add to config
    mqtt_humidity_topic = "livingroom/humidity"        
    mqtt_client = MQTTClient(
        client_id=config["mqtt.clientId"],
        server=config['mqtt.broker'],
        user=config['mqtt.user'],
        password=config['mqtt.password']
    )
    
    # main data aquisition an publishing loop
    def publish_data(timer):
        temp, hum, error = sht31.read()
        if not error:
            mqtt_client.connect()
            mqtt_client.publish(mqtt_temperature_topic, str(temp), retain=True, qos=0)
            mqtt_client.publish(mqtt_humidity_topic, str(temp) , retain=True, qos=0)
            mqtt_client.disconnect()
        else:
            print("Error reading sensor. Not publishing data")
    
    # timer = Timer()
    # timer.init(period=10000, mode=Timer.PERIODIC, callback=publish_data)

    # Wait indefinitely while the timer continues to invoke the callback function
    # while True:
    #     time.sleep(1)

# start the main function
if __name__ == "__main__":
    main()
