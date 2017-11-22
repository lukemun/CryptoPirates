import numpy as np 
import pandas as pd 
from collections import deque



def test_algorithm(filename, initialCapital):
	with open(filename, 'r') as f:
		df = pd.read_csv(f)

	closing_prices = df.iloc[:,1]
	btc_data = closing_prices.as_matrix()
	
	# Short moving average, keeps track of last sma_length data points
	sma_length = 15
	sma_data = deque()
	sma = 0
	# Large moving average, keeps track of last lma_length data points
	lma_length = 50
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

	# Now, iterate through remaining data points, generating buy and sell signals
	for val in btc_data[lma_length:]:
		print("Net worth: " + str(cash + capitalInvested))
		# Update short moving average
		sma_data.popleft()
		sma_data.append(val)
		sma = np.mean(sma_data)
		# Update large moving average
		lma_data.popleft()
		lma_data.append(val)
		lma = np.mean(lma_data)

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




test_algorithm('btc_5mins_1month_window.csv', 1000)













