import threading
import requests as req

def getPrice(url, payload):
	threading.Timer(5, getPrice, (url, payload)).start()
	response_json = req.get(url, params=payload)
	data = response_json.text
	prices.append(data)
	print (prices)


btc = "BTC"
usd = "USD"
payload = {"fsym": btc, "tsyms": usd}
url = "https://min-api.cryptocompare.com/data/price"

prices = []

getPrice(url, payload)


