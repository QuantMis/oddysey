from oddysey.utils import *
import sys
import pandas as pd
import time

class MomentumScalper:
    def __init__(self):
        self.paramData = initMongo('paramData')
        self.signalData = initMongo('signalData')

    def main(self, signal, lock):
        data = self.paramData.find_one({'name': signal['param_table']})

        mp = data['mp']
        ub = data['ub']
        lb = data['lb']

        # buy signal
        if mp > ub:
            call = "LONG"

        # sell signal
        elif mp < lb:
            call = "SHORT"

        else:
            call = "FLAT"

        # update docs
        temp_obj = {
            "signal": call,
            "timestamp":int(time.time())
        }

        print(temp_obj)

        self.updateDocs(temp_obj, signal)

        lock.release()
        return

    def updateDocs(self, data, signal):
        self.signalData.update_one({'name': signal['name']}, {"$set":data})
        return

if __name__ == '__main__':
    # init thread
    targetCol = 'signalData'
    main = MomentumScalper()
    Q = {'status':'start'}

    try:
        threadManager(main, targetCol, Q)
        
    except Exception as e:
        print(e)
        sys.exit()
