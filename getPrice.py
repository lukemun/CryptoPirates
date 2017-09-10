
# alex matthys testing 


import threading
import requests as req

btc = "BTC"
usd = "USD"
payload = {"fsym": btc, "tsyms": usd}
url = "https://min-api.cryptocompare.com/data/price"

prices = []

def getPrice(url, payload):
	threading.Timer(5, getPrice, (url, payload)).start()
	response_json = req.get(url, params=payload)
	data = response_json.text
	prices.append(data)

	# Analyze data, decide if we need a buy or sell
	analyze(prices)

	print (prices)


# Function to decide given a list of bitcoin prices whether we should buy, sell, or hold
def analyze(prices):
	pass


getPrice(url, payload)



