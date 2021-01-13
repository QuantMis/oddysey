from oddysey.utils import *
import sys
import _thread
import time

class Trader:
	def __init__(self):
		self.signalData = initMongo('strategy')

	def trade(self, config, lock):
		client = initConnector(config)
		client.updateLeverage(config['symbol'], config['leverage'])

		data = self.signalData.find_one({'name':config['signal_table'})
		signal = data['signal']
		status = config['status']

		if status == "LIVE": self.createOrder(signal)
		
		self.createOderDB(signal)

		# check config status
		# if demo -> create trades data
		# if live -> create order, create trades
		# return


	def run(self):
		while True:
			df = pd.DataFrame(list(initMongo(self.traders).find({"$or": [{"status":"DEMO"}, {"status":"LIVE"}]})))
			locks = []
			n = range(len(df))
			for i in n:
				lock = _thread.allocate_lock()
				a = lock.acquire()
				locks.append(lock)

			for i in n:
				_thread.start_new_thread(self.trade, (df.iloc[i], locks[i]))

			for i in  n:
				while locks[i].locked(): pass


if __name__ == '__main__':
	traderObj = Trader()
	try:
		traderObj.run()
	except Exception as e:
		print(e)
		sys.exit()
