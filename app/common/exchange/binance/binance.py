from typing import Dict
from binance import Client #hint
from datetime import datetime 
from common.exchange.exchange import Exchange
from settings import API_KEY_BINANCE, API_SECRET_KEY_BINANCE

class Binance(Exchange):
    client: Client = None

    def __init__(self, name):
        super().__init__(name)
        if self.client is None:
            self.create_client_binance()

    @classmethod
    def create_client_binance(cls):
        if cls.client is None:
            cls.client = Client(api_key=API_KEY_BINANCE, api_secret=API_SECRET_KEY_BINANCE)
        return cls.client
    
    def get_account_details(self, all_details: bool = False, flag_portfolio: bool = False) -> Dict[str, any]:
        account_details = self.client.get_account()
        if all_details:
            return {
                "all": account_details
                }
        if flag_portfolio:
            portfolio = list(filter(lambda x: float(x["free"]) > 0.1, account_details["balances"]))
            for p in portfolio:
                p[p["asset"]] = p["free"]
                del p["free"]
            all_pairs = list(map(lambda x: x["asset"], portfolio))
            return {
                "portfolio": portfolio, 
                "assets": all_pairs 
            }
        raise Exception("please select an option (eg: all_details or flag_portfolio)")

    def get_spot_pair(self, first_pair: str = "BTC", second_pair: str = "USDT", interval: str = "1m"):
        if first_pair == "USDT":
            return 1.0
        symbol = f'{first_pair+second_pair}'
        try:
            return self.client.get_klines(symbol=symbol, interval=interval, limit=1)[0][4]
        except Exception as e:
            print(f"Cannot get this symbol {symbol}")
            return 0
        
    def get_ticker_data(self, symbol, time_basis='1m', limit=5):
        try:
            ticker_data = self.client.get_klines(symbol=symbol, interval=time_basis, limit=limit)
            formatted_data = self._format_ticker_data(ticker_data)
            return formatted_data
        except Exception as e:
            print(f"Error retrieving ticker data: {e}")
            return None

    def _format_ticker_data(self, ticker_data):
        formatted_data = []
        for entry in ticker_data:
            timestamp = datetime.utcfromtimestamp(entry[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
            open_price = float(entry[1])
            high_price = float(entry[2])
            low_price = float(entry[3])
            close_price = float(entry[4])
            volume = float(entry[5])

            formatted_entry = {
                'timestamp': timestamp,
                'open_price': open_price,
                'high_price': high_price,
                'low_price': low_price,
                'close_price': close_price,
                'volume': volume
            }

            formatted_data.append(formatted_entry)

        return formatted_data
        
    def execute_order(quantity: float, pair: str, buy: bool, order_type: str):
        pass