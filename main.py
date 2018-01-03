import queue
from threading import Thread 
import utils
import time
import analysis
import transactor
import numpy as np

def main():

	configs = utils.loadConfigs()
	crypto = analysis.anal_object("USDT_BTC", 300, configs)

	crypto.setup()

	trans_que = queue.Queue()

	trans = transactor.TransactorThread("USDT_BTC", trans_que, configs)

	trans.start()

	while True:
		if (crypto.update() or True):
			print ('updated')
			trans_que.put(crypto.analyze_with(lambda x: input(), 'j'))

		time.sleep(1)

	trans.join()	

if __name__ == '__main__':
	main()


def moving_avgs(d):
	"""

	Takes in a deque of 500 data points
	Returns either Buy, Sell, or Hold

	"""
	deque_length = len(d)
	lma = np.mean(d)
	sma_start = 4 * deque_length / 5
	sma = np.mean(list(d)[sma_start:])

	if (sma - lma) / lma > 0.01:
		return "BUY"
	elif (sma - lma) / lma < -0.01:
		return "SELL"
	else:
		return "HOLD"















