import numpy as np
from auto_trading_aim.portfolio import Portfolio
class PortfolioBuilder(object):
    def __init__(self, capital, data, min_invest):
        self.capital, self.data = capital, data
        self.min_invest = min_invest
        self.n_samples = 100
        self.portfolio_list = self.generate_random_portfolios()

    def generate_random_portfolios(self):
        # Random percentage of invested capital
        perc_invest = np.random.uniform(low = self.min_invest, high=1.0, size=self.n_samples)
        # Random percentage of capital invested in each title
        perc_capital = np.random.dirichlet(alpha=np.ones(shape=len(list(self.data.keys()))), size=self.n_samples)

        portfolio_list = []
        for i in range(self.n_samples):
            # Capital for this sample
            s_capital = self.capital*perc_invest[i]
            # Title investment for this sample
            investments = perc_capital[i] * s_capital
            # Prices of title of last day
            prices = np.array([self.data[name].prices[-1] for name in self.data.keys()])
            # Quantity of each title
            alloc_quantities = np.floor(investments/prices)

            #Create portfolio
            allocation = {name: alloc_quantities[index] for index, name in enumerate(self.data.keys())}
            prices_dict = {name: self.data[name].prices for name in self.data.keys()}
            portfolio_list.append(Portfolio(allocation=allocation, prices_dict=prices_dict))

        return portfolio_list

    def min_var(self):
        var_array = np.empty(shape=self.n_samples)
        for i in range(self.n_samples):
            mkt_returns = self.portfolio_list[i].compute_value()[1]
            var_array[i] = mkt_returns.var()

        return self.portfolio_list[np.argmin(var_array)]

    def rate_mean_std(self):
        rate_array = np.empty(shape=self.n_samples)

        for i in range(self.n_samples):
            mkt_returns = self.portfolio_list[i].compute_value()[1]
            rate_array[i] = mkt_returns.mean() / mkt_returns.std()

        return self.portfolio_list[np.argmax(rate_array)]