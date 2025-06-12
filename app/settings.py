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
API_KEY_COINBASE = config["API_KEY_COINBASE"]
API_SECRET_KEY_COINBASE = config["API_SECRET_KEY_COINBASE"]
API_PASSPHRASE_COINBASE = config["API_PASSPHRASE_COINBASE"]

# MONGODB_HOST = config["MONGODB_HOST"]
# MONGODB_PORT = config["MONGODB_PORT"]
# MONGODB_URI = config["MONGODB_URI"].format(MONGODB_HOST, MONGODB_PORT)

# EXCHANGES = config["EXCHANGES"]
API_HOST = config["API_HOST"]
API_PORT = config["API_PORT"]