import queue
from threading import Thread 
import utils
import time
import analysis
import transactor
import numpy as np

def main():

	configs = utils.loadConfigs()
	analyzer = analysis.Analysis("USDT_BTC", 300, 500, configs)

	analyzer.setup()

	trans_que = queue.Queue()

	trans = transactor.TransactorThread("USDT_BTC", trans_que, True,configs)

	trans.start()

	while True:
		if (analyzer.update()):
			print ('updated')
			val = analyzer.analyze()
			print (val) 
			trans_que.put(val)
		time.sleep(60)

	trans.join()	

if __name__ == '__main__':
	main()












