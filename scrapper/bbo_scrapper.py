import _thread
import pandas as pd
from datetime import datetime as dt
import time
from oddysey.utils import *
import sys

import json

class BBOScrapper:
    def __init__(self):
        self.col = 'marketData'
        self.mongo_client = initMongo(self.col)

        # class params
        self.table_limit = 1000


    def getBBO(self, scrapper, lock):
        connector = initConnector(scrapper)
        res = connector.getBBO(scrapper['symbol'])
        data = {
            'ask': float(res['asks'][0][0]),
            'bid': float(res['bids'][0][0]),
            'ask_volume': float(res['asks'][0][1]),
            'bid_volume': float(res['bids'][0][1]),
            'timestamp': str(dt.fromtimestamp(res['T']/1000))
        }

        print(data)
        self.updateDocs(data, scrapper)

        lock.release()
        return

    def updateDocs(self, data, scrapper):
        # to do
        docs = self.mongo_client.find_one({'name':scrapper['name']})
        if docs['init'] is False:
            columns = ['ask', 'bid', 'ask_volume', 'bid_volume', 'timestamp']
            for i in columns:
                docs[i].append(data[i])

                if len(docs[i]) > self.table_limit:
                    docs[i].pop(0)

            temp_obj = {
                "ask": docs['ask'],
                "bid": docs['bid'],
                "ask_volume": docs['ask_volume'],
                "bid_volume": docs['bid_volume'],
                "timestamp": docs['timestamp']
            }

            self.mongo_client.update_one({'name':scrapper['name']}, {"$set":temp_obj})
            return

        else:
            ask = [data['ask']]
            bid = [data['bid']]
            ask_volume = [data['ask_volume']]
            bid_volume = [data['bid_volume']]
            timestamp = [data['timestamp']]

            temp_obj = {
                'name': scrapper['name'],
                'symbol': scrapper['symbol'],
                "ask": ask,
                "bid": bid,
                "ask_volume": ask_volume,
                "bid_volume": bid_volume,
                "timestamp": timestamp,

				# init False
				"init": False
            }
            self.mongo_client.update_one({'name':scrapper['name']}, {"$set":temp_obj})
            return



    def run(self):
        while True:
            df = pd.DataFrame(list(initMongo(self.col).find()))
            locks = []
            n = range(len(df))
            for i in n:
                lock = _thread.allocate_lock()
                a = lock.acquire()
                locks.append(lock)

            for i in n:
                _thread.start_new_thread(self.getBBO, (df.iloc[i], locks[i])) 

            for i in n:
                while locks[i].locked(): pass

if __name__ == "__main__":
    scraperObj = BBOScrapper()
    try:
        scraperObj.run()
    except Exception as e:
        print(e)
        sys.exit()
