import pandas as pd

from app.common.exchange.coinbase import coinbase
from common.exchange.exchange import Exchange

# Function to calculate technical indicators
def calculate_technical_indicators(ticker, source="coinbase", start=2020, end="2025", granularity="one_day"):
    """
    Add 10 technical analysis features to the DataFrame.
    Assumes df has columns: open_price, high_price, low_price, close_price, volume.
    """
    try:
        print(f"Adding feature to {ticker} from {source}")
        df = pd.read_csv(f"./process/backtest/histo/{ticker}_{start}_{end}_{source}_{granularity}.csv")
        # Ensure the DataFrame is sorted by timestamp
        df = df.sort_index()

        # 1. SMA (20-period)
        df['SMA_20'] = df['close_price'].rolling(window=20).mean()

        # 2. EMA (20-period)
        df['EMA_20'] = df['close_price'].ewm(span=20, adjust=False).mean()

        # 3. RSI (14-period)
        delta = df['close_price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI_14'] = 100 - (100 / (1 + rs))

        # 4-6. MACD, Signal Line, Histogram
        ema_12 = df['close_price'].ewm(span=12, adjust=False).mean()
        ema_26 = df['close_price'].ewm(span=26, adjust=False).mean()
        df['MACD'] = ema_12 - ema_26
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']

        # 7. Bollinger Bands (20-period, 2 std)
        df['BB_Middle'] = df['close_price'].rolling(window=20).mean()
        df['BB_Std'] = df['close_price'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + 2 * df['BB_Std']
        df['BB_Lower'] = df['BB_Middle'] - 2 * df['BB_Std']
        df = df.drop(columns=['BB_Std'])  # Drop intermediate column

        # 8. ATR (14-period)
        tr1 = df['high_price'] - df['low_price']
        tr2 = abs(df['high_price'] - df['close_price'].shift())
        tr3 = abs(df['low_price'] - df['close_price'].shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        df['ATR_14'] = tr.rolling(window=14).mean()

        # 9. Stochastic Oscillator (%K, 14-period)
        lowest_low = df['low_price'].rolling(window=14).min()
        highest_high = df['high_price'].rolling(window=14).max()
        df['Stochastic_K'] = 100 * (df['close_price'] - lowest_low) / (highest_high - lowest_low)

        # 10. OBV
        df['OBV'] = (df['volume'] * ((df['close_price'] > df['close_price'].shift()).astype(int) * 2 - 1)).cumsum()

        df.to_csv(f"./process/backtest/histo/TA/{ticker}_{start}_{end}_{source}_{granularity}_feature.csv")
        print(f"Hisotrized {ticker} with new features")
    except:
        print(f"An error while processing {ticker}")
        
        
# Function to process a single ticker
def process_ticker(ticker, exchange: Exchange, source="coinbase",start="01-01-2025", end="02-01-2025", granularity="one_day"):
    try:
        print(f"Starting {ticker}")
        res = exchange.get_ticker_data(ticker, start=start, end=end)
        df = pd.DataFrame(res)
        df = df.set_index(df["timestamp"]).drop(["timestamp"], axis=1)
        df.sort_index().to_csv(f"./process/backtest/histo/{ticker}_{start}_{end}_{source}_{granularity}.csv")
        print(f"{ticker} historized")
    except Exception as e:
        print(f"Issue when historizing {ticker}: {str(e)}")

