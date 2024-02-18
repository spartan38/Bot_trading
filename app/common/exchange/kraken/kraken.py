from typing import Dict, List
from krakenex import API
from datetime import datetime

from common.exchange.exchange import Exchange
from settings import API_KEY_KRAKEN, API_SECRET_KEY_KRAKEN

class Kraken(Exchange):
    api: API = None

    def __init__(self, name):
        super().__init__(name)
        if self.api is None:
            self.create_api_kraken()

    @classmethod
    def create_api_kraken(cls):
        if cls.api is None:
            cls.api = API(key=API_KEY_KRAKEN, secret=API_SECRET_KEY_KRAKEN)
        return cls.api
    
    def get_account_details(self, all_details: bool = False, flag_portfolio: bool = False) -> Dict[str, any]:
        account_details = self.api.query_private('Balance')
        if 'error' in account_details:
            if isinstance(account_details['error'], list) and len(account_details['error']) > 1:
                raise Exception(f"Error retrieving account details: {account_details['error']}")

        if all_details:
            return {
                "all": account_details["result"]
            }
        if flag_portfolio:
            portfolio = []
            for k, v in account_details["result"].items():
                if float(v) > 0.1:
                    portfolio.append({
                        k: v, 
                        "asset": k
                    })
            all_pairs = list(map(lambda x: x["asset"], portfolio))
            return {
                "portfolio": portfolio, 
                "assets": all_pairs 
            }
        raise Exception("please select an option (e.g., all_details or flag_portfolio)")

    def get_spot_pair(self, first_pair: str = "BTC", second_pair: str = "USD", interval: str = "1"):
        if first_pair == "USDT":
            return 1.0
        symbol = f'{first_pair}{second_pair}'
        try:
            klines = self.api.query_public('OHLC', {'pair': symbol, 'interval': interval})
            return float(klines['result'][list(klines['result'].keys())[0]][-1][4])
        except Exception as e:
            print(f"Error getting data for symbol {symbol}: {e}")
            return 0
        
    def execute_order(self, quantity: float, pair: str, buy: bool, order_type: str):
        # Implement order execution for Kraken
        # You may use the 'AddOrder' API method with appropriate parameters
        pass

    def get_ticker_data(self, symbol: str, time_basis: str ='1m', limit: int=5):
        try:
            ticker_data = self.api.query_public('OHLC', {'pair': symbol, 'interval': time_basis})
            print(ticker_data)
            formatted_data = self._format_ticker_data(ticker_data['result'][symbol], limit)
            return formatted_data
        except Exception as e:
            print(f"Error retrieving ticker data: {e}")
            return None

    def _format_ticker_data(self, ticker_data: List[any], limit: int):
        formatted_data = []
        for entry in ticker_data[-limit:]:
            timestamp = datetime.utcfromtimestamp(entry[0]).strftime('%Y-%m-%d %H:%M:%S')
            open_price = float(entry[1])
            high_price = float(entry[2])
            low_price = float(entry[3])
            close_price = float(entry[4])
            volume = float(entry[6])

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

    def get_available_pairs(self):
        try:
            asset_pairs = self.api.query_public('AssetPairs')
            print(asset_pairs['result'].keys())
            if 'error' in asset_pairs:
                raise Exception(f"Error retrieving asset pairs: {asset_pairs['error']}")
            if 'result' not in asset_pairs or not asset_pairs['result']:
                raise Exception("No asset pairs found")
            return list(asset_pairs['result'].keys())
        except Exception as e:
            print(f"Error getting available pairs: {e}")
            return []