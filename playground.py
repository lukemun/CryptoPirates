import poloniex

polo = poloniex.Poloniex('V20UK9TF-KYTPEBAP-4R70MIUE-H7ZP5HOR', '434eb5661ffc81dc42047301eb4b0965e6f76a8c552becf858738b0387583f487bcde51466cb9661bdd8aabb6013763862645b2a82ba43da42f7e3110815bd36')

balance = polo.returnBalances()
val = polo.__call__('returnTicker', {})

print (val)

print("I have %s ETH!" % balance['ETH'])
with open('btc.dat', 'w') as f:
	f.write(polo.marketTradeHist('BTC_USD'))
print(polo.marketTradeHist('BTC_USDT'))