# A simple test algorithm to see how much money I have in the morning after running all night
# Each time price rises from 10 seconds ago, buy one bitcoin
# Each time price decreases from 10 seconds ago, sell all (lol)

import requests as req
import time
import datetime


btc = "BTC"
usd = "USD"
payload = {"fsym": btc, "tsyms": usd}
url = "https://min-api.cryptocompare.com/data/price"


cash = 100000.0
bitcoin_owned = 0


previous = 0
while True:
	response_json = req.get(url, params=payload)
	data = response_json.json()
	data = data['USD']
	if data == previous:
		pass
	else:
		if data > previous and cash >= data:
			# purchase 1 bitcoin, get rich
			cash -= data
			bitcoin_owned += 1
		elif data < previous:
			if bitcoin_owned > 0:
				# sell all bitcoin, ABANDON SHIP
				cash += bitcoin_owned * data
				bitcoin_owned = 0
		# report on total assets
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		print "Assets: " + str(cash + bitcoin_owned*data) + " , Bitcoins Owned: " \
				+ str(bitcoin_owned) + " , Current Price: " + str(data) + \
				" , Timestamp: " + str(st)
		previous = data













