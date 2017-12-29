import numpy as np 
import pandas as pd 
from collections import deque
import matplotlib.pyplot as plt



def test_algorithm(filename, initialCapital):
	with open(filename, 'r') as f:
		df = pd.read_csv(f)
		# Play with this value to change the window with which this algorithm is run on
		df = df.iloc[:7500,:]

	closing_prices = df.iloc[:,1]
	unix_timestamps = df.iloc[:,2].as_matrix()
	btc_data = closing_prices.as_matrix()
	
	# Short moving average, keeps track of last sma_length data points
	sma_length = 100
	sma_data = deque()
	sma = 0
	# Large moving average, keeps track of last lma_length data points
	lma_length = 500
	lma_data = deque()
	lma = 0

	# Fill deques with starting data
	for indx,val in enumerate(btc_data[0:lma_length]):
		if indx > lma_length - sma_length - 1:
			sma_data.append(val)
			lma_data.append(val)
		else:
			lma_data.append(val)
	sma = np.mean(sma_data)
	lma = np.mean(lma_data)

	# Investing strategy: if sma > lma, buy in with 75% of assets. If sma < lma, sell all.
	cash = initialCapital
	capitalInvested = 0
	invested = False
	price_invested_at = 0

	# Create numpy arrays to store the sma and lma values, in order to plot these 
	sma_history = np.array([])
	lma_history = np.array([])

	# Now, iterate through remaining data points, generating buy and sell signals
	for val in btc_data[lma_length:]:
		# Calculate what our net worth is
		current_net_worth = cash
		if invested:
			gain_loss = (val - price_invested_at) / price_invested_at
			bitcoin_worth = gain_loss * capitalInvested + capitalInvested
			current_net_worth += bitcoin_worth
		print("Current Net Worth: " + str(current_net_worth))

		# Update short moving average
		sma_data.popleft()
		sma_data.append(val)
		sma = np.mean(sma_data)
		sma_history = np.append(sma_history, sma)
		# Update large moving average
		lma_data.popleft()
		lma_data.append(val)
		lma = np.mean(lma_data)
		lma_history = np.append(lma_history, lma)

		# Now decide whether to buy, sell, or simply hold
		if sma > lma and not invested:
			print("Execute Buy Order")
			# Execute a buy order, investing 75% of cash into bitcoin
			# ASSUMPTIONS: immediate transaction speed, ignoring any transaction fees or spreads 
			capitalInvested = cash * 0.75
			cash *= 0.25
			invested = True
			price_invested_at = val
		elif sma < lma and invested:
			print("Execute Sell Order")
			# Execute a sell order, selling all bitcoin assets
			# ASSUMPTIONS: immediate transaction speed, ignoring any transaction fees or spreads
			gain_loss = (val - price_invested_at) / price_invested_at
			bitcoin_worth = gain_loss * capitalInvested + capitalInvested
			cash += bitcoin_worth
			capitalInvested = 0
			invested = False
			price_invested_at = 0

	# Analyze how much money we would have had we simply invested all our capital in bitcoin and then just held
	net_worth_hold_bitcoin_instead = ((btc_data[-1] - btc_data[0]) / btc_data[0]) * initialCapital + initialCapital
	print("Net Worth had we just invested all assets in bitcoin: " + str(net_worth_hold_bitcoin_instead))


	# Plot the bitcoin prices, the sma values, and the lma values
	plt.figure()
	plt.plot(unix_timestamps, btc_data, label='BTC Price Data (closing values)')
	plt.plot(unix_timestamps[lma_length:], sma_history, label='SMA-{}'.format(str(sma_length)))
	plt.plot(unix_timestamps[lma_length:], lma_history, label='LMA-{}'.format(str(lma_length)))
	plt.xlabel('Time (Unix Timestamp)')
	plt.ylabel('Value')
	plt.title('BTC Moving Averages')
	plt.legend(loc="lower right")
	plt.show()




test_algorithm('btc_5mins_1month_window.csv', 1000)













