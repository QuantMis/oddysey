from oddysey.utils import *
import sys
import _thread
import pandas as pd
import time

class MomentumScalper:
	def __init__(self):
		self.paramData = initMongo('paramData')
		self.signalData = initMongo('strategy')

	def generate_signal(self, signal, lock):
		data = self.paramData.find_one({'name': signal['param_table']})

		mp = data['mp']
		ub = data['ub']
		lb = data['lb']

		# buy signal
		if mp > ub:
			status = "LONG"

		# sell signal
		elif mp < lb:
			status = "SHORT"

		else:
			status = "FLAT"

		# update docs
		temp_obj = {
			"status":status,
			"timestamp":int(time.time())
		}

		self.updateDocs(temp_obj, signal)

		lock.release()
		return

	def updateDocs(self, data, signal):
		self.signalData.update_one({'name': signal['name']}, {"$set":data})
		return

	def run(self):
		while True:
			df = pd.DataFrame(list(self.signalData.find()))
			locks = []
			n = range(len(df))
			for i in n:
				lock = _thread.allocate_lock()
				lock.acquire()
				locks.append(lock)

			for i in n:
				_thread.start_new_thread(self.generate_signal, (df.iloc[i], locks[i]))

			for i in n:
				while locks[i].locked(): pass

if __name__ == '__main__':
	strategyObj = MomentumScalper()
	try:
		strategyObj.run()
	except Exception as e:
		print(e)
		sys.out()

"""
trading logic + contingency

signal schema (MomentumScalper specific)

timestamp:str
status:str [flat, short, long]


"""
