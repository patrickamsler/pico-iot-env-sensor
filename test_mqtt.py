import network
import time
import ujson
from umqtt.simple import MQTTClient

# Open the JSON file for reading
with open('config.json', 'r') as file:
    # Read the contents of the file
    data = file.read()

# Parse the JSON data
config = ujson.loads(data)
print(config)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid=config['wlan.ssid'], key=config['wlan.password'])

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
    print(status)
    print('ip = ' + status[0])

c = MQTTClient(
    client_id=config["mqtt.clientId"],
    server=config['mqtt.broker'],
    user=config['mqtt.user'],
    password=config['mqtt.password']
)
c.connect()
c.publish(b"foo_topic", b"helloB", retain=True, qos=0)
time.sleep(5)
c.publish(b"foo_topic", b"helloA", retain=True, qos=0)
c.disconnect()
