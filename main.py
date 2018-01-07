import queue
from threading import Thread 
import utils
import time
import analysis
import transactor
import numpy as np

def main():

	configs = utils.loadConfigs()

	# create and initialize analysis object
	analyzer = analysis.Analysis("USDT_BTC", 300, 500, configs)
	analyzer.setup()

	# create and initialize transactor (intially holding btc)
	trans_que = queue.Queue()
	trans = transactor.TransactorThread("USDT_BTC", trans_que, True, configs)
	trans.start()

	utils.sendMsg("trader started")
	utils.write("trader started")
	while True:
		if (analyzer.update()):
			val = analyzer.analyze()
			trans_que.put(val)
		time.sleep(60)

	trans.join()	

if __name__ == '__main__':
	main()












