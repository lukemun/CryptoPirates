
# alex matthys testing 


import threading
import requests as req
import collections as c
import notifs as n

btc = "BTC"
usd = "USD"
payload = {"fsym": btc, "tsyms": usd}
url = "https://min-api.cryptocompare.com/data/price"

prices = c.deque()

def getPrice(url, payload):
	threading.Timer(10, getPrice, (url, payload)).start()
	response= req.get(url, params=payload)
	data = response.json()
	prices.append(data)
	if len(prices) > 360:
		prices.popleft()

	# Analyze data, decide if we need a buy or sell
	analyze(prices)



# Function to decide given a list of bitcoin prices whether we should buy, sell, or hold
def analyze(prices):
	last = len(prices)-1
	print (prices[last-1])
	print (prices[last])

	if abs(prices[last]['USD'] - prices[last-1]['USD'])/prices[last]['USD'] > 0.003:
		n.send_mail("%f -> %f" % (prices[last-1]['USD'], prices[last]['USD']), "alexmatthys@gmail.com")
		print ("sent mail")


getPrice(url, payload)



