"""MC1-P2: Optimize a portfolio. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
 			  		 			     			  	   		   	  			  	
Student Name: Tucker Balch (replace with your name) 			  		 			     			  	   		   	  			  	
GT User ID: yzhang3414 (replace with your User ID) 			  		 			     			  	   		   	  			  	
GT ID: 903459675 (replace with your GT ID) 			  		 			     			  	   		   	  			  	
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import pandas as pd 			  		 			     			  	   		   	  			  	
import matplotlib.pyplot as plt 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import datetime as dt 			  		 			     			  	   		   	  			  	
from util import get_data, plot_data 		
from scipy.optimize import minimize	  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
# This is the function that will be tested by the autograder 			  		 			     			  	   		   	  			  	
# The student must update this code to properly implement the functionality 			  		 			     			  	   		   	  			  	
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Read in adjusted closing prices for given symbols, date range 			  		 			     			  	   		   	  			  	
    dates = pd.date_range(sd, ed) 			  		 			     			  	   		   	  			  	
    prices_all = get_data(syms, dates)  # automatically adds SPY 			  		 			     			  	   		   	  			  	
    prices = prices_all[syms]  # only portfolio symbols 			  		 			     			  	   		   	  			  	
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later 

    # Normalization, return dataframe
    prices_norm = prices / prices.ix[0,:]
    prices_SPY_norm = prices_SPY / prices_SPY.ix[0,:]
 			  		 			     			  	   		   	  			  	
    # Define the function: cr, adr, sddr, sr
    def status(allocs):
        values = np.sum(prices_norm.values * allocs, axis = 1) # sum each row
        daily_returns = values[1:] / values[:-1] - 1.0
        cumulative_return = values[-1] / values[0] - 1.0
        average_daily_return = daily_returns.mean()
        std_daily_return = daily_returns.std()
        sharpe_ratio = np.sqrt(252) * average_daily_return / std_daily_return
        return [cumulative_return, average_daily_return, std_daily_return, sharpe_ratio]

    # Define function: - Sharp Ratio
    def sharpe_ratio(allocs):
        return -status(allocs)[-1]

    # find the allocations for the optimal portfolio 			  		 			     			  	   		   	  			  	
    # note that the values here ARE NOT meant to be correct for a test case 			  		 			     			  	   		   	  			  	
    # allocs = np.asarray([0.2, 0.2, 0.3, 0.3]) # add code here to find the allocations 			  		 			     			  	   		   	  			  	
    allocs = np.ones(len(syms))/len(syms) # initialize allocs

    # minimize
    constraints = ({'type': 'eq', 'fun': lambda inputs: 1.0 - np.sum(inputs)})
    bounds = [(0.0, 1.0)] * len(syms)
    results = minimize(sharpe_ratio, allocs, method = ('SLSQP'), bounds = bounds, constraints = constraints)
    allocs = results.x

    #cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats 			  		 			     			  	   		   	  			  	
    cr, adr, sddr, sr = status(allocs)

    # Get daily portfolio value 			  		 			     			  	   		   	  			  	
    #port_val = prices_SPY # add code here to compute daily portfolio values 			  		 			     			  	   		   	  			  	
    port_val = np.sum(prices_norm * allocs, axis = 1)
    
    # Compare daily portfolio value with SPY using a normalized plot 			  		 			     			  	   		   	  			  	
    if gen_plot: 			  		 			     			  	   		   	  			  	
        # add code to plot here 			  		 			     			  	   		   	  			  	
        df_temp = pd.concat([port_val, prices_SPY_norm], keys=['Portfolio', 'SPY'], axis=1) 
        plot_data(df_temp, title = "Daily Portfolio Value and SPY", xlabel="Date", ylabel="Price")			  		 			     			  	   		   	  			  	
        pass 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    return allocs, cr, adr, sddr, sr 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def test_code(): 			  		 			     			  	   		   	  			  	
    # This function WILL NOT be called by the auto grader 			  		 			     			  	   		   	  			  	
    # Do not assume that any variables defined here are available to your function/code 			  		 			     			  	   		   	  			  	
    # It is only here to help you set up and test your code 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Define input parameters 			  		 			     			  	   		   	  			  	
    # Note that ALL of these values will be set to different values by 			  		 			     			  	   		   	  			  	
    # the autograder! 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # start_date = dt.datetime(2009,1,1) 			  		 			     			  	   		   	  			  	
    # end_date = dt.datetime(2010,1,1) 			  		 			     			  	   		   	  			  	
    # symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM'] 
    start_date = dt.datetime(2008,6,1)                                                                              
    end_date = dt.datetime(2009,6,1)                                                                                
    symbols = ['IBM', 'X', 'GLD', 'JPM'] 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Assess the portfolio 			  		 			     			  	   		   	  			  	
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = ~False) 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Print statistics 			  		 			     			  	   		   	  			  	
    print "Start Date:", start_date 			  		 			     			  	   		   	  			  	
    print "End Date:", end_date 			  		 			     			  	   		   	  			  	
    print "Symbols:", symbols 			  		 			     			  	   		   	  			  	
    print "Allocations:", allocations 			  		 			     			  	   		   	  			  	
    print "Sharpe Ratio:", sr 			  		 			     			  	   		   	  			  	
    print "Volatility (stdev of daily returns):", sddr 			  		 			     			  	   		   	  			  	
    print "Average Daily Return:", adr 			  		 			     			  	   		   	  			  	
    print "Cumulative Return:", cr 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
if __name__ == "__main__": 			  		 			     			  	   		   	  			  	
    # This code WILL NOT be called by the auto grader 			  		 			     			  	   		   	  			  	
    # Do not assume that it will be called 			  		 			     			  	   		   	  			  	
    test_code() 			  		 			     			  	   		   	  			  	
