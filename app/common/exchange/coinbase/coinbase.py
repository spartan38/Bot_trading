from typing import Dict, List, Optional
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
                portfolio = [{"asset": k, k:v} for k, v in balances.items()]
                all_pairs = [k for k, _ in balances.items()]
                return {"portfolio": portfolio, "assets": all_pairs}
            raise Exception("Please select an option (e.g., all_details or flag_portfolio)")
        except Exception as e:
            logger.error(f"Error retrieving account details: {e}")
            raise

    def get_spot_pair(self, first_pair: str = "BTC", second_pair: str = "USD") -> Optional[float]:
        """
        Get the latest spot price for a trading pair using Coinbase Pro API.

        Args:
            first_pair: Base asset (e.g., 'BTC').
            second_pair: Quote asset (e.g., 'USD').

        Returns:
            Latest spot price as a float, or None on error.
        """
        symbol = f"{first_pair}-{second_pair}"
        try:
            # Use Coinbase Pro API's /products/<product-id>/ticker endpoint
            ticker = self.api.get_product(product_id=symbol)
            return float(ticker['price'])
        except Exception as e:
            logger.error(f"Error getting spot price for {symbol}: {e}")
            return None

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

    def get_ticker_data(self, symbol: str, time_basis: str = '60', start: str = "", end: str = "") -> List[
        Dict[str, any]]:
        """Retrieve OHLC ticker data for a symbol.

        Args:
            symbol: Trading pair (e.g., BTC-USD).
            time_basis: Candlestick interval in seconds (e.g., '60' for 1 minute).
            start: Start date in MM-DD-YYYY format.
            end: End date in MM-DD-YYYY format.

        Returns:
            List of formatted OHLC data or None on error.
        """
        if int(time_basis) not in self.VALID_INTERVALS:
            logger.error(f"Invalid time_basis {time_basis}. Valid intervals: {self.VALID_INTERVALS}")
            return None

        # Max candles per API call (API limit)
        _MAX_CANDLES = 350
        # Calculate max seconds per call for the given time_basis
        max_seconds_per_call = _MAX_CANDLES * int(time_basis)

        data = []

        try:
            start_dt = datetime.strptime(start, '%m-%d-%Y')
            end_dt = datetime.strptime(end, '%m-%d-%Y')

            # Convert time_basis to API granularity (e.g., 60 seconds = ONE_MINUTE)
            granularity = "ONE_MINUTE" if time_basis == "60" else f"{int(time_basis)}_SECONDS"

            # Current timestamp for iteration
            current_start = start_dt

            while current_start < end_dt:
                # Calculate end time for this chunk (max 350 candles)
                end_temp = min(current_start + timedelta(seconds=max_seconds_per_call), end_dt)

                candles = self.api.get_candles(
                    symbol,
                    granularity=granularity,
                    start=int(current_start.timestamp()),
                    end=int(end_temp.timestamp())
                )

                if not candles['candles']:
                    logger.warning(f"No candle data returned for {symbol} from {current_start} to {end_temp}")
                else:
                    formatted_data = self._format_ticker_data(candles['candles'])
                    data.append(formatted_data)

                # Move to the next chunk (add 1 second to avoid overlap)
                current_start = end_temp + timedelta(seconds=1)

            # Flatten the list of lists into a single list
            result = [item for sublist in data for item in sublist]
            return result

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

