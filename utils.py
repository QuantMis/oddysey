from pymongo import MongoClient
from oddysey.connector.fbinance import connector

# init mongo
def initMongo(col) -> MongoClient:
    client = MongoClient("202.59.9.188",port=27017, username="admin2", password="israa2608", authSource="admin")['oddysey'][col]
    return client

def initConnector(config):
	account = initMongo("account").find_one({"user":config["user"]})
	client = connector(account['api_key'], account['secret_key'], config['symbol'])
	return client
