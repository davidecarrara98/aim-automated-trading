from auto_trading_aim.data_loader import DataLoader
from auto_trading_aim.portfolio import Portfolio


class DataLoaderDict(object):
    def __init__(self, tickers, start, end, interval):
        self.__dict__ = {t : DataLoader(ticker=t, start=start, end=end, interval=interval) for t in tickers}

    def save(self, path):
        for t, dataloader in self.items():
            dataloader.data.to_csv(path_or_buf=f'{path}{t}.csv')

    def build_portfolio(self, allocation):
        return Portfolio(allocation=allocation, prices_dict={name:self[name].prices for name in allocation.keys()})

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
