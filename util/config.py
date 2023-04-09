import ujson
import util.logging as logging

log = logging.getLogger(__name__)

def load_config():
    # Open the JSON file for reading
    log.info("loading config")
    with open('config.json', 'r') as file:
        # Read the contents of the file
        data = file.read()

    # Parse the JSON data
    config = ujson.loads(data)
    log.debug("config loaded: " + str(config))
    return config

def save_config(config):
    # Open the JSON file for writing
    log.info("saving config")
    with open('config.json', 'w') as file:
        # Write the dictionary to the file in JSON format
        ujson.dump(config, file)
    log.debug("config saved: " + str(config))