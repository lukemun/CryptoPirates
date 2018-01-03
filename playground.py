import poloniex
import json
import time
import pandas as pd


def loadConfigs(filename='config.json'):
	with open(filename, 'r') as f:
		configs = json.load(f)
	return configs	



configs = loadConfigs()

polo = poloniex.Poloniex(configs['poloniex']['key'], configs['poloniex']['secret'], coach=True)

hist_5_mins = polo.returnChartData('USDT_BTC', 300, 1483246800, 1514437200)

df = pd.DataFrame(hist_5_mins)

print(len(hist_5_mins))

with open('btc_5mins_allof2017.csv', 'w') as f:
	df.to_csv(f)

# with open('btc_5mins.csv', 'r') as f:
# 	df2 = pd.read_csv(f)
# 	print(df2.iloc[0])










# val = polo.__call__('returnTicker', {})
# print (polo.checkCmd('returnTicker'))

# print (polo.returnTicker())
# print (polo.returnCurrencies()['BTC'])
# book = polo.returnOrderBook('usdt_btc')
# print(min(book['asks']))
# print (max(book['bids']))
# print (polo.marketTradeHist('usdt_btc'))
# print (polo.returnOpenOrders())
# print (polo.sell('USDT_BTC', '7295.00', '0.001', 'postOnly'))
# hist = polo.returnChartData('USDT_BTC', 900)
# with open('candle.txt', 'w') as out:
# 	json.dump(hist, out)
# print("I have %s ETH!" % balance['ETH'])
# with open('btc.dat', 'w') as f:
# 	f.write(polo.marketTradeHist('BTC_USD'))
# print(polo.marketTradeHist('BTC_USDT'))
