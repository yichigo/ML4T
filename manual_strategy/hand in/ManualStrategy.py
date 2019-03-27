import datetime as dt
import pandas as pd
import numpy as np
import util as ut
import random

from indicators import indicators
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
from TheoreticallyOptimalStrategy import TheoreticallyOptimalStrategy

def author():
    return 'yzhang3414'

class ManualStrategy(object):

    # constructor
    def __init__(self, verbose = False, commission = 9.95, impact=0.005):
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
        self.longs = []
        self.shorts = []
        ind = indicators(symbol, sd, ed)
        inds = ind.PSMA.copy()
        inds.columns = ['PSMA']
        inds['BB'] = ind.BB
        inds['Momentum'] = ind.Momentum
        #inds['Volatility'] = ind.Volatility
        inds = inds.dropna()
        unit = 1000
        for i, row in inds.iterrows():
            if (row['PSMA'] < 0.98) and (row['BB']<0.02) and (row['Momentum'] > -0.3): # buy signal
                self.longs.append(i)
                if hold != unit:
                    trades.ix[i,symbol] = unit - hold
                    hold = unit

            elif (row['PSMA'] > 1.02) and (row['BB']>0.98) and (row['Momentum'] < 0.3): # sell signal
                self.shorts.append(i)
                if hold != -unit:
                    trades.ix[i,symbol] = -unit - hold
                    hold = -unit

        fig = plt.figure()
        x = prices.index.values
        y = prices.values
        plt.plot(x, y/y[0], label = 'Prices', color = 'green')
        for x in self.longs:
            y = prices.ix[x,0]/prices.ix[0,0]
            plt.plot([x]*2, [y, y-0.1], color = 'blue' )
        for x in self.shorts:
            y = prices.ix[x,0]/prices.ix[0,0]
            plt.plot([x]*2, [y, y+0.1], color = 'black' )
        plt.grid(True)
        plt.legend(loc='upper left')
        plt.title('Entry Points')
        plt.tight_layout()
        plt.savefig('entrypoints_'+str(sd.year)+'.png')

        return trades

if __name__=="__main__":
    ms = ManualStrategy()
    ts = TheoreticallyOptimalStrategy()
    
    trades = ms.testPolicy( symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 1000000)
    portvals = compute_portvals(trades, start_val = 1000000, commission=9.95, impact=0.005)
    

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
    print('Manual Strategy')
    print('cum_ret',cum_ret, 'avg_daily_ret', avg_daily_ret, 'std_daily_ret', std_daily_ret)

    cum_ret_benchmark = portvals_benchmark.ix[-1] / portvals_benchmark.ix[0] - 1
    daily_ret_benchmark = portvals_benchmark / portvals_benchmark.shift(1) - 1
    avg_daily_ret_benchmark = daily_ret_benchmark.mean()
    std_daily_ret_benchmark = daily_ret_benchmark.std()
    print('Benchmark')
    print('cum_ret', cum_ret_benchmark, 'avg_daily_ret', avg_daily_ret_benchmark, 'std_daily_ret', std_daily_ret_benchmark)

#####################################################
    fig = plt.figure()
    x = portvals_benchmark.index.values
    y = portvals_benchmark.values
    plt.plot(x, y/y[0], color = 'green', label = 'Benchmark')
    x = portvals.index.values
    y = portvals.values
    plt.plot(x, y/y[0], color = 'red', label = 'Manual Strategy')
    plt.grid(True)
    plt.legend(loc='upper left')
    plt.title('Manual Strategy')
    plt.tight_layout()
    plt.savefig('ms_in.png')


#################################################TEST#################################################
#################################################TEST#################################################
    trades = ms.testPolicy( symbol = "JPM", \
        sd=dt.datetime(2010,1,1), \
        ed=dt.datetime(2011,12,31), \
        sv = 1000000)

    portvals = compute_portvals(trades, start_val = 1000000, commission=9.95, impact=0.005)


    trades_benchmark = ts.benchmark( symbol = "JPM", \
        sd=dt.datetime(2010,1,1), \
        ed=dt.datetime(2011,12,31), \
        sv = 1000000)
    portvals_benchmark = compute_portvals(trades_benchmark, start_val = 1000000, commission=0, impact=0)


#####################################################
    cum_ret = portvals.ix[-1] / portvals.ix[0] - 1
    daily_ret = portvals / portvals.shift(1) - 1
    avg_daily_ret = daily_ret.mean()
    std_daily_ret = daily_ret.std()
    print('Manual Strategy')
    print('cum_ret',cum_ret, 'avg_daily_ret', avg_daily_ret, 'std_daily_ret', std_daily_ret)

    cum_ret_benchmark = portvals_benchmark.ix[-1] / portvals_benchmark.ix[0] - 1
    daily_ret_benchmark = portvals_benchmark / portvals_benchmark.shift(1) - 1
    avg_daily_ret_benchmark = daily_ret_benchmark.mean()
    std_daily_ret_benchmark = daily_ret_benchmark.std()
    print('Benchmark')
    print('cum_ret', cum_ret_benchmark, 'avg_daily_ret', avg_daily_ret_benchmark, 'std_daily_ret', std_daily_ret_benchmark)

#####################################################
    fig = plt.figure()
    x = portvals_benchmark.index.values
    y = portvals_benchmark.values
    plt.plot(x, y/y[0], color = 'green', label = 'Benchmark')
    x = portvals.index.values
    y = portvals.values
    plt.plot(x, y/y[0], color = 'red', label = 'Manual Strategy')
    plt.grid(True)
    plt.legend(loc='upper left')
    plt.title('Manual Strategy')
    plt.tight_layout()
    plt.savefig('ms_out.png')
