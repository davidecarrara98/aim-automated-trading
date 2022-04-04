import pandas as pd
import matplotlib.pyplot as plt
from auto_trading_aim.asset import Asset

class Portfolio(object):
    def __init__(self, allocation=None, prices_dict=None):

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

    def to_df(self):
        dict_to_df = {name : [self[name].volume_owned] for name in self.keys()}
        df = pd.DataFrame.from_dict(dict_to_df, orient='columns')
        return df

    def __add__(self, other):
        allocation = {k: self.get_quantity(k) + other.get_quantity(k) for k in set(self.__dict__) | set(other.__dict__)}
        prices_dict1 = {name: self[name].prices for name in self.keys()}
        prices_dict2 = {name: other[name].prices for name in other.keys()}
        prices_dict = {**prices_dict1, **prices_dict2}
        return Portfolio(allocation=allocation, prices_dict=prices_dict)

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

    def get_quantity(self, instance):
        try:
            quantity = self.__dict__.get(instance).volume_owned
        except AttributeError:
            quantity = 0
        return quantity

    def get_prices(self, instance):
        try:
            prices = self.__dict__.get(instance).prices
        except  KeyError:
            prices = 0
        return prices

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
