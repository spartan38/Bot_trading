import yaml

with open("config.yaml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

API_KEY_BINANCE = config["API_KEY_BINANCE"]
API_SECRET_KEY_BINANCE = config["API_SECRET_KEY_BINANCE"]
API_KEY_KRAKEN = config["API_KEY_KRAKEN"]
API_SECRET_KEY_KRAKEN = config["API_SECRET_KEY_KRAKEN"]

MONGODB_URI = config["MONGODB_URI"]

EXCHANGE = config["EXCHANGE"]
API_HOST = config["API_HOST"]
API_PORT = config["API_PORT"]