from pymongo import MongoClient
from oddysey.connector.fbinance import connector
import time, uuid, _thread, pandas
from datetime import datetime

# init mongo
def initMongo(col) -> MongoClient:
    client = MongoClient("202.59.9.188",port=27017, username="admin2", password="israa2608", authSource="admin")['oddysey'][col]
    return client

# init API connector
def initConnector(config):
    account = initMongo("accountData").find_one({"name":config["account"]})
    client = connector(account['api_key'], account['secret_key'], config['symbol'])
    return client

def threadManager(cls, targetCol, Q):
    while True:
        df = pandas.DataFrame(list(initMongo(targetCol).find(Q)))
        locks = []
        n = range(len(df))
        for i in n:
            lock = _thread.allocate_lock()
            a = lock.acquire()
            locks.append(lock)

        for i in n:
            _thread.start_new_thread(cls.main, (df.iloc[i], locks[i])) 

        for i in n:
            while locks[i].locked(): pass


def createOrderDB(signal, config, order):
    tradesObj = {
        "trader": config['name'],
        "signal": config['signal'],
        "symbol": config['symbol'],
        "timestamp": signal['timestamp'],
        "id": uniqueId(),
        "side": signal['signal'],
        "order_type": order['type'],
        "status": "open",
        "qty": order['qty'],
        "open_price": getBBO(config['symbol'], signal['signal']),
        "close_price": 0,
        "closed_by": "",
        "pnl":0,
        "pnl_updated_ts":0
    }
    
    col = "liveTradesData" if config['status']=='LIVE' else "demoTradesData"
    initMongo(col).insert_one(tradesObj)
    return 

def createOrderExchange(signal):
    pass

def getBBO(symbol, signal):
    side = 'asks' if signal == "LONG" else "bids" 
    return float(connector('api', 'sec', symbol).getBBO(symbol)[side][0][0])


def is_valid(signal):        
    validWindow = 5 
    return True if (int(time.time()) - int(signal['timestamp']) <= validWindow) else False 

def uniqueId():
    return uuid.uuid4()

def utc_timestamp():
    return datetime.utcfromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')



