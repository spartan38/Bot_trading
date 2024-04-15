import pandas as pd
import time
import datetime
class ProcessStock():
    @staticmethod
    def run():
        stock1 = pd.read_csv("./process/comparative/data/AAPL.csv")
        stock2 = pd.read_csv("./process/comparative/data/TSLA.csv")

        stock1["Date"] = stock1["Date"].astype('datetime64[ns]')
        stock2["Date"] = stock2["Date"].astype('datetime64[ns]')

        stock1 = stock1[["Date", "Adj Close"]].values.tolist()
        stock2 = stock2[["Date", "Adj Close"]].values.tolist()

        return {
            "stock-1": stock1,
            "stock-2": stock2,
        }


