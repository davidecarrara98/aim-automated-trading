import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

class DataLoader(object):
    def __init__(self, ticker, start, end, interval):
        self.ticker = ticker
        self.start, self.end, self.interval = start, end, interval
        #I store data because I don't know what we specifically want to save with the method in data_loader_dict
        self.data = yf.Ticker(ticker).history(start=self.start, end=self.end, interval=self.interval)
        self.prices, self.volumes = self.data['Close'], self.data['Volume']

    def plot(self, key):
        if key not in ['Prices', 'Volumes', 'Close', 'Volume']:
            raise NameError('Information not stored')
        if key == 'Prices' or key == 'Close':
            self.prices.plot()
        if key == 'Volumes' or key == 'Volume':
            self.volumes.plot()

        plt.show()

        return

    def __str__(self):
        return f'{self.ticker} data from {self.start} to {self.end}, {self.interval} \n' \
               f'Close -> min : {self.prices.min()} max : {self.prices.max()} mean : {self.prices.mean()} \n' \
               f'   first day : {self.prices.iloc[0]} last day : {self.prices.iloc[-1]} \n' \
               f'Volume -> min : {self.volumes.min()} max : {self.volumes.max()} mean : {self.volumes.mean()} \n' \
               f'   first day : {self.volumes.iloc[0]} last day : {self.volumes.iloc[-1]} \n'

