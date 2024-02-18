from typing import List

class Exchange: 
    def __init__(self, name) -> None:
        self.name = name

    def get_account_details(self, all_details: bool = False, flag_portfolio: bool = False):
        raise NotImplementedError("Not implemented here")
    
    def get_spot_pair(self, first_pair: str = "BTC", second_pair: str = "USD", interval: str = "1m"):
        raise NotImplementedError("Not implemented here")
    
    def get_ticker_data(self, symbol: str, time_basis: str ='1m', limit: int=5):
        raise NotImplementedError("Not implemented here")
    
    def _format_ticker_data(self, ticker_data: List[any], limit: int):
        raise NotImplementedError("Not implemented here")
    
    def execute_order(quantity: float, pair: str, buy: bool, order_type: str):
        raise NotImplementedError("Not implemented here")