import pandas as pd
from oddysey.utils import *
from statistics import *
import sys

class StdDev:
	def __init__(self):
		self.col1 = 'marketData'
		self.col2 = 'paramData'

	def main(self, table, lock):
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

	
if __name__ == "__main__":

    # init thread
    targetCol = 'paramData'
    main = StdDev()
    Q = {'status':'start'}

    try:
        threadManager(main, targetCol, Q)
        
    except Exception as e:
        print(e)
        sys.exit()
	
