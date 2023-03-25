import network
import time
from umqtt.simple import MQTTClient

ssid = 'Salt_2GHz_1ACAA4'
password = ''

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])


c = MQTTClient(
    client_id="test_client",
    server="192.168.1.2",
    user="iot",
    password=""
)
c.connect()
c.publish(b"foo_topic", b"helloB", retain=True, qos=0)
time.sleep(5)
c.publish(b"foo_topic", b"helloA", retain=True, qos=0)
c.disconnect()
