import pandas as pd
import _thread
from oddysey.utils import *
from statistics import *

class StdDev:
	def __init__(self):
		self.col1 = 'marketData'
		self.col2 = 'paramData'

	def computeSTDEV(self, table, lock):
		data = initMongo(self.col1).find_one({'name': table['table_name']})

		# todo: compute params
		ask, bid = data['ask'], data['bid']
		mid_price = [round((i+j)/2,2) for i,j in zip(ask,bid)]

		# params computation exclude cuurent data
		current_mp = mid_price[-1]
		mid_price.pop(-1)

		dev = stdev(mid_price[-int(table['period']):])
		xmean = mean(mid_price[-int(table['period']):])

		data = {
			"ub":xmean+2*dev,
			"lb":xmean-2*dev,
			"mp":current_mp,
		}

		self.updateDocs(data, table)

		lock.release()
		return

	def updateDocs(self, data, table):
		docs = initMongo(self.col2).find_one({'name':table['name']})
		print(docs)
		if docs['init'] is False:
			initMongo(self.col2).update_one({'name':table['name']}, {"$set":data})

		else:
			temp_obj = {
				"name":table['name'],
				"table_name": table['table_name'],
				"period": str(table['period']),
				"lb": data['lb'],
				"ub": data['ub'],
				"mp": data['mp'],
                "init": False
			}

			initMongo(self.col2).update_one({'name':table['name']}, {"$set":temp_obj})

		return

	def run(self):
		df = pd.DataFrame(list(initMongo(self.col2).find()))
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
