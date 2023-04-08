from wireless.wifi import Wifi
from wireless.server import Server
import util.logging as logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout) # log to console
for handler in logging.getLogger().handlers:
    handler.setFormatter(logging.Formatter("[%(levelname)s] - %(name)s - %(message)s"))

print("Connecting to wifi ...")
wifi = Wifi(
    ssid="Salt_2GHz_1ACAA4",
    password="afdzJzFT9YWLKbq6zt"
)
wifi.connect()
print("wifi connected")

server = Server()
server.listen_forever()