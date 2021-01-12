from oddysey.utils import *
import sys
import _thread
import time

class Trader:
	def __init__(self):
		self.signalData = initMongo('strategy')

	def entry(self):

	def run(self):
		while True:
			df = 

if __name__ == '__main__':
	traderObj = Trader()
	try:
		traderObj.run()
	except Exception as e:
		print(e)
		sys.exit()
