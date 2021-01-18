from oddysey.utils import *
from oddysey.portfolio.sizing import SizingLibrary

import sys
import time
import logging
import pandas as pd

class basicEntry:
    def __init__(self):
        self.signalData = initMongo('signalData')
        self.entryAlgo = "protoMan"
        self.trader = 'traderData'
        self.account = 'accountData'

    def checkInventory(self, config):
        inventory = initMongo(self.account).find_one({'name':config['account']})

        if inventory['inventoryValueUsdt'] < config['firstThreshold']*inventory['initialValueUsdt']:
            
            Q = {'name':config['name']}
            update = {'maxMargin':1}

            initMongo(self.trader).find_one_and_update(Q, {"$set":update})
            
        return 

    def main(self, config, lock):
        self.checkInventory(config)
        
        signal = self.signalData.find_one({'name':config['signal']})
        marginMaximised = True if config['orderCount'] <= config['maxOrderBatch'] else False
        print(f"timestamp: {utc_timestamp()} ====> running trader: {config['name']} , orderOpen: {config['orderCount']}")

        if signal['signal'] == "LONG" and not marginMaximised:
            if is_valid(signal):
                
                order = {
                    'type':'MARKET',            
                    'qty':SizingLibrary(config, signal['signal']).returnVal()
                }
                createOrderDB(signal, config, order)
                Q = {'name':config['name']}
                update = {
                    "orderCount":1 
                }

                initMongo(self.trader).find_one_and_update(Q, {"$inc":update})

        lock.release()
        return 
    
if __name__ == '__main__':

    # init thread
    targetCol = 'traderData'
    main = basicEntry()
    Q = {'entryAlgo':main.entryAlgo}

    try:
        threadManager(main, targetCol, Q)
        
    except Exception as e:
        print(e)
        sys.exit()
