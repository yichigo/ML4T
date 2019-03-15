"""Assess a betting strategy. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
 			  		 			     			  	   		   	  			  	
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
  		 			     			  	   		   	  			  	
def author(): 			  		 			     			  	   		   	  			  	
        return 'yzhang3414' # replace tb34 with your Georgia Tech username. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def gtid(): 			  		 			     			  	   		   	  			  	
	return 903459675 # replace with your GT ID number 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def get_spin_result(win_prob): 			  		 			     			  	   		   	  			  	
	result = False 			  		 			     			  	   		   	  			  	
	if np.random.random() <= win_prob: 			  		 			     			  	   		   	  			  	
		result = True 			  		 			     			  	   		   	  			  	
	return result 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def test_code(): 			  		 			     			  	   		   	  			  	
	win_prob = 18.0/38.0 # set appropriately to the probability of a win 			  		 			     			  	   		   	  			  	
	np.random.seed(gtid()) # do this only once 			  		 			     			  	   		   	  			  	
	print get_spin_result(win_prob) # test the roulette spin 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
	# add your code here to implement the experiments 			  		 			     			  	   		   	  			  	
def simulator(bankroll): # if bankroll <= 0, unlimited
	win_prob = 18.0/38.0 # for American wheel
	winnings = np.zeros(1000+1)

	episode_winnings = 0
	i = 0
	while episode_winnings < 80: # here we set the goal = $80
		won = False
		bet_amount = 1
		while not won:
			i = i + 1
			won = get_spin_result(win_prob)
			if won:
				episode_winnings = episode_winnings + bet_amount
			else:
				episode_winnings = episode_winnings - bet_amount
				bet_amount = bet_amount * 2
				if bankroll > 0: # check if next bet_amount exceed the bankroll
					bet_amount = min(bet_amount, bankroll + episode_winnings)

			winnings[i] = episode_winnings
			if i == 1000: # reach the time limit
				return winnings

			if bet_amount == 0: # reach the bankroll limit
				winnings[i+1:1001] = winnings[i] # fill the remains
				return winnings

	winnings[i+1:1001] = winnings[i] # fill the remains
	return winnings

def exp_plot_all(n, bankroll, fn): # run n times, fn is file name
	# Plot all the Trials, for Figure 1
	# Run n times, where n = 10
	plt.clf()
	for i in range(n):
		winnings = simulator(bankroll)
		plt.plot(winnings, label = 'Trial ' + str(i+1))
	plt.xlim(0, 300)
	plt.ylim(-256, 100)
	plt.xlabel('Spins')
	plt.ylabel('Winnings')
	plt.legend(loc='lower right')
	plt.savefig(fn)

def exp_plot_mean_median(n, bankroll, fn_mean, fn_median): # run n times, fn is file name
	# Run n times, where n = 1000
	winnings_n = np.zeros((n,1000+1))
	for i in range(n):
		winnings_n[i] = simulator(bankroll)
	winnings_mean = np.mean(winnings_n, axis=0)
	std = np.std(winnings_n, axis=0)
	winnings_median = np.median(winnings_n, axis=0)

	# Plot Mean, and Mean +- Stdev, for Figure 2 and 4
	plt.clf()
	plt.plot(winnings_mean, label='Mean')
	plt.plot(winnings_mean + std, label='Mean + Stdev')
	plt.plot(winnings_mean - std, label='mean - Stdev')
	plt.xlim(0, 300)
	plt.ylim(-256, 100)
	plt.xlabel('Spins')
	plt.ylabel('Winnings')
	plt.legend(loc='lower right')
	plt.savefig(fn_mean)

	# Plot Median, and Median +- Stdev, for Figure 3 and 5
	plt.clf()
	plt.plot(winnings_median, label='Median')
	plt.plot(winnings_median + std, label='Median + Stdev')
	plt.plot(winnings_median - std, label='Median - Stdev')
	plt.xlim(0, 300)
	plt.ylim(-256, 100)
	plt.xlabel('Spins')
	plt.ylabel('Winnings')
	plt.legend(loc='lower right')
	plt.savefig(fn_median)

	winrate_80 = np.sum(winnings_n[:,-1] == 80, axis=0)/(n+0.0)
	print('\nProbability of winning $80: '+ str(winrate_80))
	print('Mean after '+ str(n) +' bets: '+ str(winnings_mean[-1]))
	print('Median after '+ str(n) +' bets: '+ str(winnings_median[-1]))
	print('Stdev after '+ str(n) +' bets: '+ str(std[-1]))

if __name__ == "__main__": 			  		 			     			  	   		   	  			  	
	test_code()

	# experiment1
	# Run 10 times for Figure 1, with unlimited bankroll
	exp_plot_all(10, 0, 'Figure_1.png')
	# Run 1000 times for Figure 2, 3, with unlimited bankroll
	exp_plot_mean_median(1000, 0, 'Figure_2.png','Figure_3.png')
	# experiment2
	# Run 1000 times for Figure 4, 5, with bankroll = 256
	exp_plot_mean_median(1000, 256, 'Figure_4.png', 'Figure_5.png')

	# exp_plot_all(100, 256, 'Figure_11.png')