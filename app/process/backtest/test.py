from app.common.exchange.exchange_factory import exchange_factory
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from app.process.backtest.utils import calculate_technical_indicators, process_ticker

coinbase = exchange_factory("coinbase")





# Main execution
pairs = coinbase.get_available_pairs()
tickers = [t for t in pairs if t.split("-")[1] == "USD"]

# Set max number of concurrent threads (adjust based on your system and API limits)
max_workers = 3

# Use ThreadPoolExecutor for multithreading
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Submit all ticker processing tasks
    executor.map(process_ticker, tickers, "coinbase")
    executor.map(calculate_technical_indicators, tickers)


print("All tickers processed")
