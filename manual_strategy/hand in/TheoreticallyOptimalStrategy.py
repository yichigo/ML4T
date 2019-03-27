import datetime as dt
import pandas as pd
import numpy as np
import util as ut
import random

from marketsimcode import compute_portvals
import matplotlib.pyplot as plt

def author():
    return 'yzhang3414'

class TheoreticallyOptimalStrategy(object):

    # constructor
    def __init__(self, verbose = False, commission = 0.0, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.commission = commission

    def testPolicy(self, symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 1000000):

        dates = pd.date_range(sd, ed)
        symbols = [symbol]
        prices_all = ut.get_data(symbols, dates)  # automatically adds SPY
        prices = prices_all[symbols] # use [symbols] to remove SPY 

        # initial
        trades = prices.copy()
        trades.ix[:,:] = 0
        hold = 0

        for i in range(len(prices)-1): # no tomorrow for last day
            price_today = prices.ix[i,symbol]
            price_tomorrow = prices.ix[i+1,symbol]
            if price_tomorrow > price_today:
                trades.ix[i,symbol] = 1000 - hold
                hold = 1000
            elif price_tomorrow < price_today:
                trades.ix[i,symbol] = -1000 - hold
                hold = -1000

        return trades

    def benchmark(self, symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 1000000):

        dates = pd.date_range(sd, ed)
        symbols = [symbol]
        prices_all = ut.get_data(symbols, dates)  # automatically adds SPY
        prices = prices_all[symbols] # use [symbols] to remove SPY 

        # initial
        trades = prices.copy() 
        trades.ix[:,:] = 0
        trades.ix[0,:] = 1000

        return trades

if __name__=="__main__":
    ts = TheoreticallyOptimalStrategy()
    trades = ts.testPolicy( symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 1000000)
    portvals = compute_portvals(trades, start_val = 1000000, commission=0, impact=0)

    trades_benchmark = ts.benchmark( symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 1000000)
    portvals_benchmark = compute_portvals(trades_benchmark, start_val = 1000000, commission=0, impact=0)

#####################################################
    cum_ret = portvals.ix[-1] / portvals.ix[0] - 1
    daily_ret = portvals / portvals.shift(1) - 1
    avg_daily_ret = daily_ret.mean()
    std_daily_ret = daily_ret.std()
    print('Theoretically Optimal Strategy')
    print('cum_ret',cum_ret, 'avg_daily_ret', avg_daily_ret, 'std_daily_ret', std_daily_ret)

    cum_ret_benchmark = portvals_benchmark.ix[-1] / portvals_benchmark.ix[0] - 1
    daily_ret_benchmark = portvals_benchmark / portvals_benchmark.shift(1) - 1
    avg_daily_ret_benchmark = daily_ret_benchmark.mean()
    std_daily_ret_benchmark = daily_ret_benchmark.std()
    print('Benchmark')
    print('cum_ret', cum_ret_benchmark, 'avg_daily_ret', cum_ret_benchmark, 'std_daily_ret', cum_ret_benchmark)

#####################################################
    fig = plt.figure()
    x = portvals_benchmark.index.values
    y = portvals_benchmark.values
    plt.plot(x, y/y[0], color = 'green', label = 'Benchmark')
    x = portvals.index.values
    y = portvals.values
    plt.plot(x, y/y[0], color = 'red', label = 'Theoretically Optimal Strategy')
    plt.grid(True)
    plt.legend(loc='upper left')
    plt.title('Theoretically Optimal Strategy')
    plt.tight_layout()
    plt.savefig('ts_in.png')
    

