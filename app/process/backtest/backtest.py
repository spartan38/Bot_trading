import pandas as pd 
from typing import Any

class Backtest:
    def __init__(self, data: Any, capital: float):
        self.data = data
        self.capital = 100_000.0
        self.position = 0

    def apply_strategy(self):
        pass

    def execute_trades(self):
        pass

    def calculate_returns(self):
        pass

    def visualize_results(self):
        pass