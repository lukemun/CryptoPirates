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
		self.polo = poloniex.Poloniex(configs['poloniex']['key'],
							 configs['poloniex']['secret'], coach=True)

	def setup(self, data_file):
		with open(data_file, 'r') as f:
			self.crypto_hist = pd.read_json(f.read())
		# just 24 hours
		max_len = int((24*60*60)/self.period)
		self.deq = deque((row for index, row in self.crypto_hist[:max_len].iterrows()), maxlen=max_len)
		self.crypto_hist_index = len(self.deq)


	def analyzeWith(self, analysis_func, args=False):
		momentum = [0]*(self.crypto_hist_index)
		while (self.crypto_hist_index != len(self.crypto_hist-1)):
			if (args):
				moment = analysis_func(self.deq, *args)
			else:
				moment = analysis_func(self.deq)
			momentum.append(moment)
			self.deq.append(self.crypto_hist.iloc[self.crypto_hist_index])
			self.crypto_hist_index += 1
		self.crypto_hist['momentum'] = momentum


	def analyze(self, analysis_func, args=False):
		if (args):
			moment = analysis_func(self.deq, *args)
		else:
			moment = analysis_func(self.deq)
		return moment

	def analyzeOn(self, analysis_func, args=False):
		momentum = [0]*(self.crypto_hist_index)
		while (self.crypto_hist_index != len(self.crypto_hist-1)):
			if (args):
				moment = analysis_func(self.deq, *args)
			else:
				moment = analysis_func(self.deq)
			momentum.append(moment)
			self.deq.append(self.crypto_hist.iloc[self.crypto_hist_index])
			self.crypto_hist_index += 1
		self.crypto_hist['momentum2'] = momentum

	def reset(self):
		# just 24 hours
		max_len = int((24*60*60)/self.period)
		self.deq = deque((row for index, row in self.crypto_hist[:max_len].iterrows()), maxlen=max_len)
		self.crypto_hist_index = len(self.deq)


	def getHist(self):
		return self.crypto_hist

	def getHistIndex(self):
		return self.crypto_hist_index

	def getDeq(self):
		return self.deq