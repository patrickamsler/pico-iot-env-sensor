import socket
import util.logging as logging
from util.config import load_config, save_config
import json
import ujson

log = logging.getLogger(__name__)


class Server:
    def __init__(self, port=80):
        addrinfo = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        self.socket = socket.socket()
        self.socket.bind(addrinfo)
        self.socket.listen(1)
        log.info(f"server listening on {addrinfo}")

    def listen_forever(self):
        while True:
            client, addr = self.socket.accept()
            log.info(f"client connected from {addr}")
            try:
                request = client.recv(1024)
                response = self.__handle_request(request)
                client.send(response)
                client.close()
            except Exception as e:
                log.error(e)
                client.close()

    def __handle_request(self, request):
        verb, path, body = self.__parseRequest(request)

        if path == "/":
            return self.__response(body="Hello from Raspberry Pi Pico!")
        elif verb == "GET" and path == "/status":
            return self.__status_response()
        elif verb == "GET" and path == "/config":
            return self.__config_response()
        elif verb == "POST" and path == "/config":
            return self.__update_config(body)
        else:
            return self.__response(status=404, body="Not Found")

    def __parseRequest(self, request):
        # Split the request into its components
        request_str = request.decode("utf-8")
        request_lines = request_str.split("\n")
        verb = request_lines[0].split(" ")[0]
        path = request_lines[0].split(" ")[1]
        body = None
        if (verb == "POST"):
            body = self.__parseBody(request_str)
        return verb, path, body

    def __parseBody(self, request_str):
        body = None
        split = request_str.split("\r\n\r\n")
        if (len(split) > 1):
            body = split[1]
        return body

    def __response(self, status=200, body=None, content_type="text/html"):
        return f"HTTP/1.1 {status}\r\nContent-Type: {content_type}\r\n\r\n{body}"

    def __status_response(self):
        config = self.__load_config()
        device_id = config["device_id"]
        # TODO get temp and humidity from sensor
        temp = 22.5
        hum = 50.0
        response = json.dumps({
            "temperature": temp,
            "humidity": hum,
            "device_id": device_id
        })
        return self.__response(body=response, content_type="application/json")

    def __config_response(self):
        config = self.__load_config()
        response = json.dumps(config)
        return self.__response(body=response, content_type="application/json")

    def __update_config(self, body):
        if not body:
            return self.__response(status=400, body="Invalid config")

        new_config = ujson.loads(body)
        current_config = self.__load_config()

        # does new config have the same fields as current config?
        if not set(new_config.keys()) == set(current_config.keys()):
            return self.__response(status=400, body="Invalid config")

        save_config(new_config)

        response = json.dumps(new_config)
        return self.__response(status=201, body=response, content_type="application/json")

    def __load_config(self):
        config = load_config()
        # Check if any key in the configuration contains the string 'password'
        for key in config:
            if 'password' in key:
                config[key] = '********'
        return config
