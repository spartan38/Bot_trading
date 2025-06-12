from typing import Dict, List
from coinbase.rest import RESTClient
from datetime import datetime, timedelta
import logging

from app.settings import API_KEY_COINBASE, API_SECRET_KEY_COINBASE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Coinbase:
    api: RESTClient = None
    VALID_INTERVALS = [60, 300, 900, 3600, 21600, 86400]  # Coinbase candlestick intervals in seconds (1m, 5m, 15m, 1h, 6h, 1d)

    def __init__(self, name: str):
        self.name = name
        if self.api is None:
            self.create_api_coinbase()

    @classmethod
    def create_api_coinbase(cls) -> RESTClient:
        """Initialize the Coinbase Advanced Trade API client."""
        if cls.api is None:
            cls.api = RESTClient(
                api_key=API_KEY_COINBASE,
                api_secret=API_SECRET_KEY_COINBASE
            )
        return cls.api

    def get_account_details(self, all_details: bool = False, flag_portfolio: bool = False, min_balance: float = 0.1) -> Dict[str, any]:
        """Retrieve account balance details.

        Args:
            all_details: If True, return all balance details.
            flag_portfolio: If True, return portfolio with assets above min_balance.
            min_balance: Minimum balance threshold for portfolio filtering.

        Returns:
            Dictionary containing account details or portfolio.

        Raises:
            Exception: If API error occurs or invalid options selected.
        """
        try:
            accounts = self.api.get_accounts()
            balances = {account['available_balance']['currency']: float(account['available_balance']['value']) for account in accounts['accounts']}

            if all_details:
                return {"all": balances}
            if flag_portfolio:
                portfolio = [{"asset": asset, "amount": amount} for asset, amount in balances]
                all_pairs = [x["asset"] for x in portfolio]
                return {"portfolio": portfolio, "assets": all_pairs}
            raise Exception("Please select an option (e.g., all_details or flag_portfolio)")
        except Exception as e:
            logger.error(f"Error retrieving account details: {e}")
            raise

    def get_spot_pair(self, first_pair: str = "BTC", second_pair: str = "USD", interval: str = "60") -> float:
        """Get the latest spot price for a trading pair.

        Args:
            first_pair: Base asset (e.g., BTC).
            second_pair: Quote asset (e.g., USD).
            interval: Candlestick interval in seconds (e.g., 60 for 1 minute).

        Returns:
            Latest closing price or 0.0 on error.
        """
        if first_pair == "USDT" and second_pair == "USD":
            return 1.0
        if int(interval) not in self.VALID_INTERVALS:
            logger.error(f"Invalid interval {interval}. Valid intervals: {self.VALID_INTERVALS}")
            return 0.0

        symbol = f"{first_pair}-{second_pair}"
        try:
            candles = self.api.get_candles(symbol, granularity=int(interval))
            if not candles.get('candles'):
                raise Exception("No candle data returned")
            return float(candles['candles'][-1]['close'])  # Latest close price
        except Exception as e:
            logger.error(f"Error getting data for symbol {symbol}: {e}")
            return 0.0

    def execute_order(self, quantity: float, pair: str, buy: bool, order_type: str = "market") -> Dict[str, any]:
        """Execute a buy or sell order on Coinbase.

        Args:
            quantity: Order volume (in base asset).
            pair: Trading pair (e.g., BTC-USD).
            buy: True for buy order, False for sell.
            order_type: Order type (e.g., 'market', 'limit').

        Returns:
            Dictionary with order details or error.

        Raises:
            Exception: If API error occurs.
        """
        try:
            if order_type == "market":
                order = self.api.market_order(
                    client_order_id=f"{pair}_{'buy' if buy else 'sell'}_{datetime.now().timestamp()}",
                    product_id=pair,
                    side='BUY' if buy else 'SELL',
                    base_size=str(quantity)
                )
            elif order_type == "limit":
                raise NotImplementedError("Limit orders require a price parameter")
            else:
                raise ValueError(f"Unsupported order type: {order_type}")

            if 'error' in order:
                raise Exception(f"Error executing order: {order.get('error')}")
            logger.info(f"Order executed: {order}")
            return order
        except Exception as e:
            logger.error(f"Error executing order for {pair}: {e}")
            return {'error': str(e)}

    def get_ticker_data(self, symbol: str, time_basis: str = '60', start: str = "", end: str = "") -> List[Dict[str, any]]:
        """Retrieve OHLC ticker data for a symbol.

        Args:
            symbol: Trading pair (e.g., BTC-USD).
            time_basis: Candlestick interval in seconds.
            limit: Number of recent entries to return.

        Returns:
            List of formatted OHLC data or None on error.
        """
        if int(time_basis) not in self.VALID_INTERVALS:
            logger.error(f"Invalid time_basis {time_basis}. Valid intervals: {self.VALID_INTERVALS}")
            return None
        _MAX_CALL = 300
        data = []
        try:
            start = datetime.strptime(start, '%m-%d-%Y')
            end = datetime.strptime(end, '%m-%d-%Y')
            diff = end - start
            for i in range(0, diff.days, _MAX_CALL):
                start_temp = start + timedelta(days=i)
                end_temp = start + timedelta(days=i + _MAX_CALL)
                if end_temp>end:
                    end_temp = end
                candles = self.api.get_candles(symbol, granularity="ONE_DAY", start=int(start_temp.timestamp()), end=int(end_temp.timestamp()))
                if not candles['candles']:
                    raise Exception("No candle data returned")
                formatted_data = self._format_ticker_data(candles['candles'])
                data.append(formatted_data)
            r = []
            for i in range(0, len(data)):
                r += data[i]

            return r
        except Exception as e:
            logger.error(f"Error retrieving ticker data for {symbol}: {e}")
            return None

    def _format_ticker_data(self, ticker_data: List[Dict]) -> List[Dict[str, any]]:
        """Format raw OHLC data into a structured format.

        Args:
            ticker_data: Raw OHLC data from Coinbase API.
            limit: Number of recent entries to include.

        Returns:
            List of formatted OHLC entries.
        """
        formatted_data = []
        for entry in ticker_data:
            formatted_entry = {
                'timestamp': datetime.utcfromtimestamp(int(entry['start'])).strftime('%Y-%m-%d %H:%M:%S'),
                'open_price': float(entry['open']),
                'high_price': float(entry['high']),
                'low_price': float(entry['low']),
                'close_price': float(entry['close']),
                'volume': float(entry['volume']),
            }
            formatted_data.append(formatted_entry)
        return formatted_data

    def get_available_pairs(self) -> List[str]:
        """Retrieve all available trading pairs on Coinbase.

        Returns:
            List of trading pair symbols or empty list on error.
        """
        try:
            products = self.api.get_products()
            return [product['product_id'] for product in products['products']]
        except Exception as e:
            logger.error(f"Error getting available pairs: {e}")
            return []

