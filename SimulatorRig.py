import pandas as pd
import json
import utils
import poloniex
from collections import deque

class SimRig():

	def __init__(self, currency, period, configs):
		self.period = period
		self.currency = currency
		self.deq = None
		self.crypto_hist = None
		self.crypto_hist_index = 0 
		self.analysis_func = None
		self.polo = poloniex.Poloniex(configs['poloniex']['key'],
							 configs['poloniex']['secret'], coach=True)
		self.crypto_analysis = None

	def setup(self, data_file):
		with open(data_file, 'r') as f:
			self.crypto_hist = pd.read_json(f.read())
		self.crypto_analysis = self.crypto_hist
		# just 24 hours
		max_len = int((24*60*60)/self.period)
		self.deq = deque((row for index, row in self.crypto_hist[:max_len].iterrows()), maxlen=max_len)
		self.crypto_hist_index = len(self.deq)


	def analyzeWith(self, analysis_func, args=False):
		self.analysis_func = analysis_func
		momentum = [0]*(self.crypto_hist_index)
		while (self.crypto_hist_index != len(self.crypto_hist-1)):
			if (args):
				moment = self.analysis_func(self.deq, *args)
			else:
				moment = self.analysis_func(self.deq)
			momentum.append(moment)
			self.deq.append(self.crypto_hist.iloc[self.crypto_hist_index])
			self.crypto_hist_index += 1
		self.crypto_analysis['momentum'] = momentum

	def reset(self):
		self.crypto_analysis = self.crypto_hist
		# just 24 hours
		max_len = int((24*60*60)/self.period)
		self.deq = deque((row for index, row in self.crypto_hist[:max_len].iterrows()), maxlen=max_len)
		self.crypto_hist_index = len(self.deq)

            
	def getAnalysis(self):
		return self.crypto_analysis

	def getHist(self):
		return self.crypto_hist

	def getHistIndex(self):
		return self.crypto_hist_index

	def getDeq(self):
		return self.deq