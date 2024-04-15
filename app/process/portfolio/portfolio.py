from typing import Dict, List, Any

from common.exchange.exchange_factory import exchange_factory


def get_portfolio(exchanges: List[str] = ["binance", "kraken"]) -> List[Dict[str, Any]]:
    my_portfolio = []
    for exchange in exchanges:
        exchange_object = exchange_factory(exchange)
        balance_account = exchange_object.get_account_details(all_details=False, flag_portfolio = True)
        spots = {}
        for asset in balance_account["assets"]:
            symbol = f"{asset}USDT"
            spot = exchange_object.get_spot_pair(first_pair=asset)
            spots[symbol] = float(spot) if spot else -1
        for line in balance_account["portfolio"]:
            symbol = f"{line['asset']}USDT"
            float_free = float(line[line['asset']])
            line["quantity"] = float_free
            line["exchange"] = exchange
            if float_free > 0.1 and symbol in spots:
                line["amount_usd"] = spots[symbol] * float_free if spots[symbol] > 0 else 0
            else:
                line["amount_usd"] = None
            my_portfolio.append(line)
        del spots
    return my_portfolio