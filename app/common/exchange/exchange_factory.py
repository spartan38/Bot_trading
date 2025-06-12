from common.exchange.exchange import Exchange
from common.exchange.binance.binance import Binance
from common.exchange.kraken.kraken import Kraken

from app.common.exchange.coinbase.coinbase import Coinbase


def exchange_factory(exchange_used: str) -> Exchange:
    if exchange_used == "binance":
        return Binance("binance")
    elif exchange_used == "kraken":
        return Kraken("kraken")
    elif exchange_used == "coinbase":
        return Coinbase("coinbase")
    else:
        raise Exception("Exchange Unknown")