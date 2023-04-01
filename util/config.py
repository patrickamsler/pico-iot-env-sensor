import ujson

def load_config():
    # Open the JSON file for reading
    print("load config file")
    with open('config.json', 'r') as file:
        # Read the contents of the file
        data = file.read()

    # Parse the JSON data
    config = ujson.loads(data)
    print("config loaded:", config)
    return config