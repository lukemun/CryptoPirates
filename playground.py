import poloniex
import json


def loadConfigs(filename='config.json'):
	with open(filename, 'r') as f:
		configs = json.load(f)
	return configs	


configs = loadConfigs()

polo = poloniex.Poloniex(configs['poloniex']['key'], configs['poloniex']['secret'], coach=True)

balance = polo.returnBalances()


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
hist = polo.returnChartData('USDT_BTC', 900)
with open('candle.txt', 'w') as out:
	json.dump(hist, out)
# print("I have %s ETH!" % balance['ETH'])
# with open('btc.dat', 'w') as f:
# 	f.write(polo.marketTradeHist('BTC_USD'))
# print(polo.marketTradeHist('BTC_USDT'))
