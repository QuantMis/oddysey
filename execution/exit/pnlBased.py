from oddysey.utils import *
from oddysey.sizing import SizingLibrary

import sys
import _thread
import time
import pandas as pd

class MomentumEntry:
    def __init__(self):
        self.signalData = initMongo('signalData')
        self.entryAlgo = "MomentumEntry"
        self.trader = 'traderData'

    # entry logic 
    def entry(self, config, lock):
        client = initConnector(config)
        #client.updateLeverage(config['symbol'], config['leverage'])

        signal = self.signalData.find_one({'name':config['signal']})
        print(signal)

        if signal['status'] != "FLAT":
            if is_valid(signal):
                self.createOrderDB(signal, config)
                self.createOrderExchange(signal)

        lock.release()
        return 

    def createOrderDB(self, signal, config):

        try:
            trades = initMongo(self.trader).find_one({"name":config['name']})['tradesData']

        except Exception as e:
            trades = []


        trade = {
            "timestamp": signal['timestamp'],
            "id": uniqueId(),
            "side": signal['status'],
            "status": "open",
            "qty": SizingLibrary(config).returnVal(),
            "open_price": getBBO(config['symbol'], signal['status']),
            "close_price": 0,
            "closed_by": "",
        }

        trades.append(trade)
        
        temp_obj = {
            "name": config['name'],
            "entryAlgo": self.entryAlgo,
            "symbol": config['symbol'],
            "account": config['account'],
            "tradesData": trades
        }
        initMongo(self.trader).find_one_and_update({'name':config['name']}, {'$set':temp_obj})
        return 

    def createOrderExchange(self, signal):
        pass


    def run(self):
        while True:
            Q = {
                '$and' : [
                         { 
                           '$or' : [ 
                                   {"status": "LIVE"},
                                   {"status" : "DEMO"}
                                 ]
                         },
                         { 
                           "entryAlgo":self.entryAlgo
                         }
                       ]
            } 

            df = pd.DataFrame(list(initMongo(self.trader).find({'entryAlgo':self.entryAlgo})))
            locks = []
            n = range(len(df))
            for i in n:
                lock = _thread.allocate_lock()
                a = lock.acquire()
                locks.append(lock)

            for i in n:
                _thread.start_new_thread(self.entry, (df.iloc[i], locks[i]))

            for i in  n:
                while locks[i].locked(): pass


if __name__ == '__main__':
    entryAlgo = MomentumEntry()
    try:
        entryAlgo.run()
    except Exception as e:
        print(e)
        sys.exit()
