import threading
import queue
import poloniex
import pandas as pd

class TransactorThread(threading.Thread):
	"""TransactorThread, polls queue for actions.
		Then interacts with poloniex api to buy/sell"""

	def __init__(self, currency, trans_q, configs):
		super().__init__()
		self.currency = currency
		self.trans_q = trans_q
		self.stoprequest = threading.Event()
		self.polo = poloniex.Poloniex(configs['poloniex']['key'],
						 configs['poloniex']['secret'], coach=True)


	def run(self):
		""" Initiated with start()"""
		while not self.stoprequest.isSet():
			try:
				print ("trying")
				action = self.trans_q.get(True)
				if (action == "buy"):
					print ("here")
					self.buy()
				elif (action == "sell"):
					self.sell()
			except queue.Empty:
				print ("empty")
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
	    volume = wallet["USDT"]["btcValue"]
	    return self.polo.buy("USDT_BTC", btc_price, volume)

	# limit taker sell
	def sell(self, strength=None):
	    wallet = self.getBalancesDict()
	    orders = self.polo.returnOrderBook(self.currency)
	    bids = pd.DataFrame(orders["bids"], columns=["price", "volume"]).astype(float)
	    btc_price = getWeightedAvg(bids)
	    # no need to calc volume since out btc is volume
	    volume = wallet["BTC"]["btcValue"]
	    return self.polo.sell("USDT_BTC", btc_price, volume)

	def join(self, timeout=None):
		self.stoprequest.set()
		super().join(timeout)


def getWeightedAvg(df):
    tot_vol = df["volume"].sum()
    weight = df["price"] * df["volume"]
    return weight.sum()/tot_vol


# unused
def exchangeAvgDiff(asks, bids):
    askAvg = weighted_avg(asks)
    bidAvg = weighted_avg(bids)
    return (askAvg - bidAvg)/bidAvg