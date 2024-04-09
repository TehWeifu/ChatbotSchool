from pymongo import MongoClient
from tabulate import tabulate

from cfg.mongo_cfg import *

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@mycluster.xkgnpk7.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"
client = MongoClient(uri)
db = client.rasa
conversations = db.conversations

pipeline = [
    {"$unwind": "$events"},
    {"$match": {"events.event": "user", "events.parse_data.intent.name": {"$exists": True}}},
    {"$group": {"_id": "$events.parse_data.intent.name", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]

results = conversations.aggregate(pipeline)

print("Most common intents")
print(tabulate(results, headers="keys", tablefmt="pretty"))

client.close()
