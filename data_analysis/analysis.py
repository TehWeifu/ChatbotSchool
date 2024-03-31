from pymongo import MongoClient

uri = "mongodb+srv://rasa:Qwe_1234@mycluster.xkgnpk7.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"
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
for result in results:
    print(result)
