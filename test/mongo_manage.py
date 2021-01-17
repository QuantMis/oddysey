from oddysey.utils import *
from pprint import pprint
import time
import random

# know collections
paramData = "paramData"
traderData = "traderData"
signalData = "signalData"

trader = initMongo(traderData).find()[0]

"""# working unit test
trades = col['tradesData']
n_trades = trades[-1]

print("before", n_trades)

Q = {'name':'ethMomentumTest', 'tradesData.id':n_trades['id']}
update = {"tradesData.$.status":"open"}

testUpdate = initMongo(traderData).find_one_and_update(Q, {"$set":update})
print("after", initMongo(traderData).find()[0]['tradesData'][-1])
"""

# check time update all orders at one
# each trader will be handle by separate thread

# first method
# fetch using mongodb (deep nested)

Q = {"name":"ethMomentumTest", "tradesData.status":"open"}
data = initMongo(traderData).find_one(Q)
tradesData = data['tradesData']
pprint(tradesData)
print(len(tradesData))


"""
# second method
# fetch all tradesData
# get id for all tradesData that is not closed

pnl = random.uniform(-1,1)

# not a good practice 
# if can, dont do linear scan, use mongodb indexing
# imagine if you have 10000 of trades data. you need to loop each one haaa

ids = [i['id'] for i in trader['tradesData'] if i['status'] == 'open']
print(ids)
print(len(ids))
"""

