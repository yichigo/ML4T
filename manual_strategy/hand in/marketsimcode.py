import pandas as pd 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import datetime as dt 			  		 			     			  	   		   	  			  	
import os 			  		 			     			  	   		   	  			  	
from util import get_data, plot_data 			  		 			     			  	   		   	  			  	

def author():
    return 'yzhang3414'

def compute_portvals(df_trades, start_val = 1000000, commission=9.95, impact=0.005): 			  		 			     			  	   		   	  			  	
    # orders	  		 			     			  	   		   	  			  	
    #orders = pd.read_csv(orders_file, index_col = 'Date', parse_dates = True, na_values=['nan'])
    
    trades = df_trades.copy()
    start_date = trades.index.min()
    end_date = trades.index.max()
    dates = get_data(['SPY'], pd.date_range(start_date, end_date)).index.get_values()
    
    symbols = list(trades.columns.values)
    symbol = symbols[0]

    # prices
    prices = get_data(symbols, dates)[symbols] # use [symbols] to remove SPY 
    prices['CASH'] = 1 # price of a cash is always 1
    # trades
    #trades = pd.DataFrame( columns = symbols + ['CASH'], index = dates)
    #trades = trades.fillna(value = 0)
    trades['CASH'] = 0
    
    for i, row in trades.iterrows():
        getShares = row[symbol]
        if (getShares != 0):
            shares = np.abs(getShares)
            buy = getShares/shares
            trades.ix[i, 'CASH'] -= (buy + impact)*shares*prices.ix[i, symbol] + commission

   	# holdings
    holdings = trades.cumsum()
    holdings['CASH'] += start_val
    
    # values
    values = prices * holdings
    
    portvals = values.sum(axis = 1)
    return portvals

if __name__ == "__main__": 			  		 			     			  	   		   	  			  	
    pass			  		 			     			  	   		   	  			  	
