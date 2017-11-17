import numpy as np 
import pandas as pd 
from collections import deque



def test_algorithm(filename, initialCapital):
	with open(filename, 'r') as f:
		df = pd.read_csv(f)

	closing_prices = df.iloc[:,1]
	btc_data = closing_prices.as_matrix()
	
	# Short moving average, keeps track of last 5 data points
	sma_data = deque()
	sma = 0
	# Medium moving average, keeps track of last 15 data points
	mma_data = deque()
	mma = 0
	# Large moving average, keeps track of last 30 data points
	lma_data = deque()
	lma = 0

	# Fill deques with starting data
	for indx,val in enumerate(btc_data[0:30]):
		if indx > 24:
			sma_data.append(val)
			mma_data.append(val)
			lma_data.append(val)
		elif indx > 14:
			mma_data.append(val)
			lma_data.append(val)
		else:
			lma_data.append(val)
	sma = np.mean(sma_data)
	mma = np.mean(mma_data)
	lma = np.mean(lma_data)

	# Now, iterate through remaining data points, generating buy and sell signals
	for val in btc_data[30:]:
		pass




test_algorithm('btc_5mins.csv', 1000)













