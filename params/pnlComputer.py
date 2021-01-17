from oddysey.utils import *
from oddysey.utils import *
import pandas as pd
import _thread
import sys

class computePnl:
    def __init__(self):
       self.liveTradesData = 'liveTradesData' 
       self.demoTradesData = 'demoTradesData'

    def main(self, config, lock):
        # to do
        # fetch trades open data from respective col
        # logic to compute pnl ??
        # compute and update

        Q = {'status':'open'}
        ids = initMongo(config).find(Q)
        
        for i in ids:
            
            print(i['id'])
            #bulk.find( { '_id':  id}).update({ '$set': {  "isBad" : "N" }})
            #bulk.execute() 

        lock.release()
        return

    def run(self):
        # process live and demo trades data in two separate thread
        n_col = [self.liveTradesData, self.demoTradesData]
        locks = []
        n = range(len(n_col))

        for i in n:
            lock = _thread.allocate_lock()
            a =  lock.acquire()
            locks.append(lock)

        for i in n:
            lock = _thread.start_new_thread(self.main, (n_col[i], locks[i]))

        for i in n:
            while locks[i].locked(): pass

if __name__ == '__main__':

    try:
        computePnl().run()
    except Exception as e:
        print(e)
        sys.exit(0)
