"""MC2-P1: Market simulator. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Copyright 2018, Georgia Institute of Technology (Georgia Tech) 			  		 			     			  	   		   	  			  	
Atlanta, Georgia 30332 			  		 			     			  	   		   	  			  	
All Rights Reserved 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Template code for CS 4646/7646 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Georgia Tech asserts copyright ownership of this template and all derivative 			  		 			     			  	   		   	  			  	
works, including solutions to the projects assigned in this course. Students 			  		 			     			  	   		   	  			  	
and other users of this template code are advised not to share it with others 			  		 			     			  	   		   	  			  	
or to make it available on publicly viewable websites including repositories 			  		 			     			  	   		   	  			  	
such as github and gitlab.  This copyright statement should not be removed 			  		 			     			  	   		   	  			  	
or edited. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
We do grant permission to share solutions privately with non-students such 			  		 			     			  	   		   	  			  	
as potential employers. However, sharing with other current or future 			  		 			     			  	   		   	  			  	
students of CS 7646 is prohibited and subject to being investigated as a 			  		 			     			  	   		   	  			  	
GT honor code violation. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
-----do not edit anything above this line--- 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Student Name: Yichao Zhang (replace with your name) 			  		 			     			  	   		   	  			  	
GT User ID: yzhang3414 (replace with your User ID) 			  		 			     			  	   		   	  			  	
GT ID: 903459675 (replace with your GT ID) 			  		 			     			  	   		   	  			  	
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import pandas as pd 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import datetime as dt 			  		 			     			  	   		   	  			  	
import os 			  		 			     			  	   		   	  			  	
from util import get_data, plot_data 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def author():
    return 'yzhang3414'

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005): 			  		 			     			  	   		   	  			  	
    # this is the function the autograder will call to test your code 			  		 			     			  	   		   	  			  	
    # NOTE: orders_file may be a string, or it may be a file object. Your 			  		 			     			  	   		   	  			  	
    # code should work correctly with either input 			  		 			     			  	   		   	  			  	
    # TODO: Your code here 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # In the template, instead of computing the value of the portfolio, we just 			  		 			     			  	   		   	  			  	
    # read in the value of IBM over 6 months 			  		 			     			  	   		   	  			  	
    # start_date = dt.datetime(2008,1,1) 			  		 			     			  	   		   	  			  	
    # end_date = dt.datetime(2008,6,1) 			  		 			     			  	   		   	  			  	
    # portvals = get_data(['IBM'], pd.date_range(start_date, end_date)) 			  		 			     			  	   		   	  			  	
    # portvals = portvals[['IBM']]  # remove SPY 			  		 			     			  	   		   	  			  	
    # rv = pd.DataFrame(index=portvals.index, data=portvals.as_matrix()) 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # return rv 		

    # orders	  		 			     			  	   		   	  			  	
    orders = pd.read_csv(orders_file, index_col = 'Date', parse_dates = True, na_values=['nan'])
    
    start_date = orders.index.min()
    end_date = orders.index.max()
    dates = get_data(['SPY'], pd.date_range(start_date, end_date)).index.get_values()
    symbols = orders['Symbol'].unique().tolist()

    # prices
    prices = get_data(symbols, dates)[symbols] # use [symbols] to remove SPY 
    prices['CASH'] = 1 # price of a cash is always 1
    
    # trades
    trades = pd.DataFrame( columns = symbols + ['CASH'], index = dates)
    trades = trades.fillna(value = 0)
    for i, row in orders.iterrows():
    	symbol = row['Symbol']
    	shares = row['Shares']
    	buy = 1 if (row['Order'] == 'BUY') else -1
    	trades.ix[i, symbol] += buy*shares
    	trades.ix[i, 'CASH'] -= (buy + impact)*shares*prices.ix[i, symbol] + commission
   	
   	# holdings
    holdings = trades.cumsum()
    holdings['CASH'] += start_val
    
    # values
    values = prices * holdings
    
    portvals = values.sum(axis = 1)
    return portvals
 			  		 			     			  	   		   	  			  	
def test_code(): 			  		 			     			  	   		   	  			  	
    # this is a helper function you can use to test your code 			  		 			     			  	   		   	  			  	
    # note that during autograding his function will not be called. 			  		 			     			  	   		   	  			  	
    # Define input parameters 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    of = "./orders/orders-02.csv" 			  		 			     			  	   		   	  			  	
    sv = 1000000 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Process orders 			  		 			     			  	   		   	  			  	
    portvals = compute_portvals(orders_file = of, start_val = sv) 			  		 			     			  	   		   	  			  	
    if isinstance(portvals, pd.DataFrame): 			  		 			     			  	   		   	  			  	
        portvals = portvals[portvals.columns[0]] # just get the first column 			  		 			     			  	   		   	  			  	
    else: 			  		 			     			  	   		   	  			  	
        "warning, code did not return a DataFrame" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Get portfolio stats 			  		 			     			  	   		   	  			  	
    # Here we just fake the data. you should use your code from previous assignments. 			  		 			     			  	   		   	  			  	
    # start_date = dt.datetime(2008,1,1) 			  		 			     			  	   		   	  			  	
    # end_date = dt.datetime(2008,6,1) 			  		 			     			  	   		   	  			  	
    # cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5] 			  		 			     			  	   		   	  			  	
    # cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5] 			  		 			     			  	   		   	  			  	
 	
    start_date = portvals.index.min()
    end_date = portvals.index.max()
    cum_ret = portvals.ix[-1] / portvals.ix[0] - 1
    daily_ret = portvals / portvals.shift(1) - 1
    avg_daily_ret = daily_ret.mean()
    std_daily_ret = daily_ret.std()
    sharpe_ratio = 252 ** 0.5 * (avg_daily_ret) / std_daily_ret

    prices_SPY = get_data(['SPY'], pd.date_range(start_date, end_date))
    portvals_SPY = prices_SPY.sum(axis = 1)
    cum_ret_SPY = portvals_SPY.ix[-1] / portvals_SPY.ix[0] - 1
    daily_ret_SPY = portvals_SPY / portvals_SPY.shift(1) - 1
    avg_daily_ret_SPY = daily_ret_SPY.mean()
    std_daily_ret_SPY = daily_ret_SPY.std()
    sharpe_ratio_SPY = 252 ** 0.5 * (avg_daily_ret_SPY) / std_daily_ret_SPY

    # Compare portfolio against $SPX 			  		 			     			  	   		   	  			  	
    print "Date Range: {} to {}".format(start_date, end_date) 			  		 			     			  	   		   	  			  	
    print 			  		 			     			  	   		   	  			  	
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio) 			  		 			     			  	   		   	  			  	
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY) 			  		 			     			  	   		   	  			  	
    print 			  		 			     			  	   		   	  			  	
    print "Cumulative Return of Fund: {}".format(cum_ret) 			  		 			     			  	   		   	  			  	
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY) 			  		 			     			  	   		   	  			  	
    print 			  		 			     			  	   		   	  			  	
    print "Standard Deviation of Fund: {}".format(std_daily_ret) 			  		 			     			  	   		   	  			  	
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY) 			  		 			     			  	   		   	  			  	
    print 			  		 			     			  	   		   	  			  	
    print "Average Daily Return of Fund: {}".format(avg_daily_ret) 			  		 			     			  	   		   	  			  	
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY) 			  		 			     			  	   		   	  			  	
    print 			  		 			     			  	   		   	  			  	
    print "Final Portfolio Value: {}".format(portvals[-1]) 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
if __name__ == "__main__": 			  		 			     			  	   		   	  			  	
    test_code() 			  		 			     			  	   		   	  			  	
