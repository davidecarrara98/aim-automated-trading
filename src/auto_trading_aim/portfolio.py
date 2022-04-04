import pandas as pd
import matplotlib.pyplot as plt
from auto_trading_aim.asset import Asset

class Portfolio(object):
    def __init__(self, allocation, prices_dict):
        self.__dict__ = {name : Asset(ticker_name=name, prices=prices_dict[name], volume_owned=quantity)
                         for name, quantity in allocation.items()}


    def __str__(self):
        ret_dict = {str(asset) for asset in self.values()}
        return str(ret_dict)

    def compute_value(self):
        prices_list = [asset.prices for asset in self.values()]
        prices_df = pd.concat(prices_list, axis=1)
        quantities = [asset.volume_owned for asset in self.values()]
        prices_df = prices_df.mul(quantities, axis=1)
        val = prices_df.sum(axis=1)
        mkt_returns = val.pct_change()

        return val, mkt_returns

    def hist(self):
        _, mkt_returns = self.compute_value()

        mkt_returns.hist()
        plt.show()

        return

    def plot(self):

        val, _ =self.compute_value()

        val.plot()
        plt.show()

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __len__(self):
        return len(self.__dict__)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def __contains__(self, item):
        return item in self.__dict__