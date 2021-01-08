import pandas as pd
import _thread
from oddysey.utils import *
from statistics import *

configs = [{'name':'eth1_stdev_20', 'table_name':'eth1', 'period':20}, {'name':'eth1_stdev_100', 'table_name':'eth1', 'period':100}]

class StdDev:
	def __init__(self):
		self.col1 = 'marketData'
		self.col2 = 'paramData'

	def computeSTDEV(self, table, lock):
		data = initMongo(self.col1).find_one({'name': table['table_name']})

		# todo: compute params
		ask, bid = data['ask'], data['bid']
		mid_price = [round((i+j)/2,2) for i,j in zip(ask,bid)][-int(table['period']):]
		dev = stdev(mid_price)
		
		# make insertion/update to docs
		docs = initMongo(self.col2).find_one({'name': table['name']})
		if docs:

		lock.release()

	def run(self):
		df = pd.DataFrame(configs)
		locks = []
		n = range(len(df))

		for i in n:
			lock = _thread.allocate_lock()
			a = lock.acquire()
			locks.append(lock)

		for i in n:
			_thread.start_new_thread(self.computeSTDEV, (df.iloc[i], locks[i]))

		for i in n:
			while locks[i].locked():pass

if __name__ == "__main__":
	pcompObj = StdDev()
	while True:
		pcompObj.run()
