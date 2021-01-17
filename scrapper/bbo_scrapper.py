import pandas as pd
from datetime import datetime as dt
import time
from oddysey.utils import *
import sys
import json

class BBOScrapper:
    def __init__(self):
        self.col = 'marketData'
        self.table_limit = 1000


    def main(self, scrapper, lock):
        run = runThread(scrapper)
        if run:
            start = int(time.time())
            connector = initConnector(scrapper)
            res = connector.getBBO(scrapper['symbol'])
            data = {
                'ask': float(res['asks'][0][0]),
                'bid': float(res['bids'][0][0]),
                'ask_volume': float(res['asks'][0][1]),
                'bid_volume': float(res['bids'][0][1]),
                'timestamp': str(dt.fromtimestamp(res['T']/1000))
            }

            self.updateDocs(data, scrapper)
            print(f"time taken getBBO and updateDocs: {int(time.time())-start}")
            lock.release()
            return
        else:
            lock.release()
            return

    def updateDocs(self, data, scrapper):
        docs = initMongo(self.col).find_one({'name':scrapper['name']})
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

            
            hey = initMongo(self.col).find_one_and_update({'name':scrapper['name']}, {"$set":temp_obj})
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
		"init": False
            }
            initMongo(self.col).find_one_and_update({'name':scrapper['name']}, {"$set":temp_obj})
            return

if __name__ == "__main__":

    # init thread
    targetCol = 'marketData'
    main = BBOScrapper()
    Q = {'status':'start'}

    try:
        threadManager(main, targetCol, Q)
        
    except Exception as e:
        print(e)
        sys.exit()
