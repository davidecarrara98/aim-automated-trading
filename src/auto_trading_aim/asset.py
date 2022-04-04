import numpy as np
import matplotlib.pyplot as plt
import auto_trading_aim.portfolio as ptf

class Asset(object):
    def __init__(self, ticker_name, prices, volume_owned):
        self.ticker_name = ticker_name
        self.prices, self.volume_owned = prices, volume_owned
        self.mkt_returns =  self.prices.pct_change(1)

    def __str__(self):
        return f'{self.ticker_name} #{self.volume_owned} | mu: {self.mkt_returns.mean()} ' \
               f'| sigma_squared: {self.mkt_returns.var()}'
    def hist(self):
        self.mkt_returns.hist()
        plt.show()
        return
