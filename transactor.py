import threading
import queue
import poloniex
import pandas as pd
import utils
import json

class TransactorThread(threading.Thread):
	"""TransactorThread, polls queue for actions.
		Then interacts with poloniex api to buy/sell"""

	def __init__(self, currency, trans_q, holding, configs):
		super().__init__()
		self.currency = currency
		self.trans_q = trans_q
		self.stoprequest = threading.Event()
		self.polo = poloniex.Poloniex(configs['poloniex']['key'],
						 configs['poloniex']['secret'], coach=True)
		self.holding = holding

	def run(self):
		""" Initiated with start()"""
		while not self.stoprequest.isSet():
			try:
				action = self.trans_q.get(True)
				# utils.write("obtained value")
				if (action == 1 and not self.holding):
					utils.write("buying")
					utils.sendMsg("buying")
					ret_val = self.buy()
					utils.write(ret_val)
					utils.sendMsg(parseTradeReturn(ret_val))
				elif (action == -1 and self.holding):
					utils.write("selling")
					utils.sendMsg("selling")
					ret_val = self.sell()
					utils.write(ret_val)
					utils.sendMsg(parseTradeReturn(ret_val))
			except queue.Empty:
				continue


	def getBalancesDict(self):
	    wallet = pd.DataFrame(self.polo.returnCompleteBalances()).astype(float)
	    return wallet

	# limit taker buy 
	def buy(self, strength=None):
	    wallet = self.getBalancesDict()
	    orders = self.polo.returnOrderBook(self.currency)
	    asks = pd.DataFrame(orders["asks"], columns=["price", "volume"]).astype(float)
	    btc_price = getWeightedAvg(asks)
	    # calc volume of btc we can buy with current usdt
	    # sell less so we are gauranteed enough balance
	    volume = wallet["USDT"]["btcValue"] * 0.98
	    ret_val = self.polo.buy("USDT_BTC", btc_price, volume)
	    self.holding = True
	    return ret_val

	# limit taker sell
	def sell(self, strength=None):
	    wallet = self.getBalancesDict()
	    orders = self.polo.returnOrderBook(self.currency)
	    bids = pd.DataFrame(orders["bids"], columns=["price", "volume"]).astype(float)
	    btc_price = getWeightedAvg(bids)
	    # no need to calc volume since out btc is volume
	    volume = wallet["BTC"]["btcValue"]
	    ret_val = self.polo.sell("USDT_BTC", btc_price, volume)
	    self.holding = False
	    return ret_val

	def join(self, timeout=None):
		self.stoprequest.set()
		super().join(timeout)


def getWeightedAvg(df):
    tot_vol = df["volume"].sum()
    weight = df["price"] * df["volume"]
    return weight.sum()/tot_vol

def parseTradeReturn(ret_val):
	trade_stats = ret_val['resultingTrades'][0]
	ret_msg = "%s %s btc at %s" % (trade_stats['type'], trade_stats['amount'], trade_stats['rate'])
	return ret_msg
