from typing import Dict
from binance import Client #hint


def get_details_account(client: Client = None, all_details: bool = False, flag_portfolio: bool = False) -> Dict[str, any]:
    if client is None:
        from settings import API_KEY_BINANCE, API_SECRET_KEY_BINANCE
        client = Client(api_key=API_KEY_BINANCE, api_secret=API_SECRET_KEY_BINANCE)

    
    account_details = client.get_account()
    if all_details:
        return {
            "all": account_details
            }
    if flag_portfolio:
        portfolio = list(filter(lambda x: float(x["free"]) > 0.1, account_details["balances"]))
        all_pairs = list(map(lambda x: x["asset"], portfolio))
        return {
            "portfolio": portfolio, 
            "assets": all_pairs 
        }
    raise Exception("please select an option (eg: all_details or flag_portfolio)")

def get_spot_pair(client: Client = None, first_pair: str = "BTC", second_pair: str = "USDT", interval: str = "1m"):
    if client is None:
        from settings import API_KEY_BINANCE, API_SECRET_KEY_BINANCE
        client = Client(api_key=API_KEY_BINANCE, api_secret=API_SECRET_KEY_BINANCE)
    
    if first_pair == "USDT":
        return 1.0
    
    symbol = f'{first_pair+second_pair}'
    try:
        return client.get_klines(symbol=symbol, interval=interval, limit=1)[0][4]
    except Exception as e:
        print(f"Cannot get this symbol {symbol}")
        return 0
