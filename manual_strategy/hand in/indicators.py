import pandas as pd
import numpy as np
import datetime as dt
import util as ut
import random
import os

import matplotlib.pyplot as plt

def author():
    return 'yzhang3414'

class indicators():
    #STD = ''
    def __init__(self, symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        lookback = 10, \
        lookback_momentum = 3):

        symbol = "JPM"
        syms=[symbol] 
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY  
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        dates = prices_SPY.index.values

        self.prices = prices_all[syms] # only portfolio symbols, drop SPY
        self.prices = self.prices/self.prices.ix[0,symbol] # Normalize
        self.lookback = lookback

        # indicator: prices / SMA
        self.STD = self.prices.rolling(window = lookback, min_periods=lookback).std()
        self.SMA = self.prices.rolling(window = lookback, min_periods=lookback).mean()
        self.PSMA = self.prices / self.SMA
        
        # indicator: BollingerBand
        self.topBand = self.SMA + (2 * self.STD)
        self.bottomBand = self.SMA - (2 * self.STD)
        self.BB = (self.prices - self.bottomBand) / (self.topBand - self.bottomBand)
        
        # indicator: Momentum
        self.Momentum = self.prices/self.prices.shift(lookback_momentum) - 1
        
        # indicator: Volatility
        self.dailyReturn = self.prices/self.prices.shift(1) -1
        self.Volatility = self.dailyReturn.rolling(window = lookback, min_periods=lookback).std()
        
        # Modify the names
        self.prices.columns = ['Price']
        self.STD.columns = ['STD']
        self.SMA.columns = ['SMA']
        self.PSMA.columns = ['Price / SMA']
        self.topBand.columns = ['Top Band']
        self.bottomBand.columns = ['Bottom Band']
        self.BB.columns = ['BBP']
        self.Momentum.columns = ['Momentum']
        self.dailyReturn.columns = ['Daily Return']
        self.Volatility.columns = ['Volatility']


if __name__=="__main__":
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    indicators = indicators(symbol = "JPM", sd = sd, ed = ed, lookback = 10)

    features = indicators.prices.copy()
    features.columns = ['Price']
    features[['SMA']] = indicators.SMA
    features[['BB']] = indicators.BB
    features[['Momentum']] = indicators.Momentum
        
    ##################################################
    fig, axes = plt.subplots(2, 1, sharex=True)
    
    indicators.prices.plot(ax = axes[0])
    indicators.SMA.plot(ax = axes[0])
    axes[0].grid(True)
    axes[0].legend(loc='lower right')

    indicators.PSMA.plot(ax = axes[1])
    axes[1].grid(True)
    axes[1].legend(loc='lower right')

    plt.tight_layout()
    fig.suptitle('Prices / SMA')
    fig.subplots_adjust(top=0.9)
    plt.savefig('PSMA_'+str(sd.year)+'.png')

    ##################################################
    fig, axes = plt.subplots(2, 1, sharex=True)
    
    indicators.prices.plot(ax = axes[0])
    indicators.topBand.plot(ax = axes[0])
    indicators.bottomBand.plot(ax = axes[0])
    axes[0].grid(True)
    axes[0].legend(loc='lower right')

    indicators.BB.plot(ax = axes[1])
    axes[1].grid(True)
    axes[1].legend(loc='lower right')
    
    plt.tight_layout()
    fig.suptitle('Bollinger Band')
    fig.subplots_adjust(top=0.9)
    plt.savefig('BB_'+str(sd.year)+'.png')

    ##################################################
    fig, axes = plt.subplots(2, 1, sharex=True)
    
    indicators.prices.plot(ax = axes[0])
    axes[0].grid(True)
    axes[0].legend(loc='lower right')

    indicators.Momentum.plot(ax = axes[1])
    axes[1].grid(True)
    axes[1].legend(loc='lower right')
    
    plt.tight_layout()
    fig.suptitle('Momentum')
    fig.subplots_adjust(top=0.9)
    plt.savefig('Momentum_'+str(sd.year)+'.png')

    ##################################################
    fig, axes = plt.subplots(2, 1, sharex=True)
    
    indicators.prices.plot(ax = axes[0])
    axes[0].grid(True)
    axes[0].legend(loc='lower right')

    indicators.dailyReturn.plot(ax = axes[1])
    indicators.Volatility.plot(ax = axes[1])
    axes[1].grid(True)
    axes[1].legend(loc='lower right')
    
    fig.suptitle('Volatility')
    plt.tight_layout()
    fig.subplots_adjust(top=0.9)
    plt.savefig('Volatility_'+str(sd.year)+'.png')


