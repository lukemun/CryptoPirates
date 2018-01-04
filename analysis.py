import pandas as pd
import utils
import poloniex
from collections import deque
import numpy as np

class Analysis(object):
	"""analysis object! stores and processes crypto data
		for the last 24 hours."""

	def __init__(self, currency, period, hist_length, configs):
		self.period = period
		self.hist_length = hist_length
		self.currency = currency
		self.deq = None
		self.polo = poloniex.Poloniex(configs['poloniex']['key'],
						 configs['poloniex']['secret'], coach=True)

	def setup(self):
		crypto_json = self.polo.returnChartData(self.currency, self.period)
		crypto_data = pd.DataFrame(crypto_json)
		self.deq = deque((row for index, row in crypto_data.iterrows()), 
															maxlen=self.hist_length)
		
	
	def update(self):
		crypto_json = self.polo.returnChartData(self.currency, self.period)
		new_crypto_data = pd.DataFrame(crypto_json)
		if new_crypto_data.iloc[len(new_crypto_data)-1]["date"] != self.deq[len(self.deq)-1]["date"]:
			# index is wrong, repeats at 287 but data is new
			self.deq.append(new_crypto_data.iloc[len(new_crypto_data)-1])
			return True
		return False


	def analyze(self):
		return int(input())		
#return moving_avgs(self.deq)

	def getDeq(self):
		return self.deq

def moving_avgs(deq):
	"""

	Takes in a deque of 500 data points
	Returns either Buy, Sell, or Hold

	"""
	d = pd.DataFrame(list(deq))['weightedAverage'].astype(float)
	deque_length = len(d)
	lma = np.mean(d)
	sma_start = int(4 * deque_length / 5)
	sma = np.mean(d[sma_start:])

	if (sma - lma) / lma > 0.01:
		return 1
	elif (sma - lma) / lma < -0.01:
		return -1
	else:
		return 0


