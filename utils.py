from pymongo import MongoClient

# init mongo
def initMongo(col) -> MongoClient:
    mClient = MongoClient("202.59.9.188",port=27017, username="admin", password="israa2608", authSource="admin")['oddysey'][col]
    return mClient

if __name__ == "__main__":
   client = initMongo()
