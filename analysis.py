import pandas as pd
import utils
import poloniex
from collections import deque

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
		if new_crypto_data.iloc[len(new_crypto_data)-1]["date"] == self.deq[len(deq)-1]["date"]:
			self.deq.append(new_crypto_data.iloc[0])
			return True
		return False

	def log(self, filename=None):
		if (filename == None):
			filename = "{0}_hist.csv".format(self.currency)
		


	def analyze_with(self, analysis_func, args=False):
		"""Pass in arguments with keys, must be mapping.
			Ex. {"alpha": 1.2, "beta":0.7}"""
		if args:
			return analysis_func(*args)
		return analysis_func()

