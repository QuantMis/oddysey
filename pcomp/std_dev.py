import pandas as pd
import _thread
from oddysey.utils import *

configs = [{'table_name':'eth1'}] #,{'table_name':'eth2'}]

class StdDev:
	def __init__(self):
		self.col1 = 'marketData'
		self.col2 = 'paramData'

	def computeSTDEV(self, table, lock):
		data = initMongo(self.col1).find_one({'name': table['table_name']})
		print(f"ts: {data['timestamp'][-1]}, ask: {data['ask'][-1]}, ask_volume: {data['ask_volume'][-1]}")
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
