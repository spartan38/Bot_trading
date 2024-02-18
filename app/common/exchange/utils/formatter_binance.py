"""
The purpose of this module is to standardise 
the output of each exchange
"""


def convert_account_details(output: dict[str, any]) -> ResultAccountDetails:
    pass

def convert_spot_pair(output: dict[str, any]) -> dict:
    ticker_pricer = {}
    for line in output["portfolio"]:
        symbol = f"{line['asset']}USDT"
        float_free = float(line["free"])
        
    
    return {
        "portfolio": ticker_pricer, 
        "assets": output["assets"]
    }

