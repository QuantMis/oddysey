from oddysey.utils import *
from oddysey.portfolio.sizing import SizingLibrary

import sys
import time
import pandas as pd

class basicEntry:
    def __init__(self):
        self.signalData = initMongo('signalData')
        self.entryAlgo = "basicEntry"
        self.trader = 'traderData'

    # entry logic 
    def main(self, config, lock):
        client = initConnector(config)
        #client.updateLeverage(config['symbol'], config['leverage'])

        signal = self.signalData.find_one({'name':config['signal']})
        print(signal)

        if signal['signal'] != "FLAT":
            if is_valid(signal):
                # create order details
                order = {
                    'type':'MARKET',            
                    'qty':SizingLibrary(config).returnVal()
                }
                createOrderDB(signal, config, order)
                createOrderExchange(signal)

        lock.release()
        return 
    
if __name__ == '__main__':

    # init thread
    targetCol = 'traderData'
    main = basicEntry()
    # Q = {'$and': [{'$or': [{'status':'DEMO'}, {'status':'LIVE'}]}, {'entryAlgo':main.entryAlgo}]}
    Q = {}

    try:
        threadManager(main, targetCol, Q)
        
    except Exception as e:
        print(e)
        sys.exit()
