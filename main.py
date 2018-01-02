import queue
from threading import Thread 
import utils
import time
import analysis
import transactor

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