from pymongo import MongoClient
from oddysey.connector.fbinance import connector
import time, uuid

# init mongo
def initMongo(col) -> MongoClient:
    client = MongoClient("202.59.9.188",port=27017, username="admin2", password="israa2608", authSource="admin")['oddysey'][col]
    return client

# init API connector
def initConnector(config):
    account = initMongo("accountData").find_one({"name":config["account"]})
    client = connector(account['api_key'], account['secret_key'], config['symbol'])
    return client

def getBBO(symbol, status):
    side = 'asks' if status == "LONG" else "bids" 
    return float(connector('api','sec',symbol).getBBO(symbol)[side][0][0])

def is_valid(signal):        
    validWindow = 5 
    return True if (int(time.time()) - int(signal['timestamp']) <= validWindow) else False 

def uniqueId():
    return uuid.uuid4()
