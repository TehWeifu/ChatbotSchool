import os

from pymongo import MongoClient
from tabulate import tabulate

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@mycluster.xkgnpk7.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"
client = MongoClient(uri)
db = client.rasa
conversations = db.conversations

# Most common intents
pipeline = [
    {"$unwind": "$events"},
    {"$match": {"events.event": "user", "events.parse_data.intent.name": {"$exists": True}}},
    {"$group": {"_id": "$events.parse_data.intent.name", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]

results = conversations.aggregate(pipeline)

print("Most common intents")
print(tabulate(results, headers="keys", tablefmt="pretty"))

# Intent Confidence Stats
pipeline_confidence = [
    {"$unwind": "$events"},
    {"$match": {"events.event": "user"}},
    {"$group": {"_id": "$events.parse_data.intent.name",
                "average_confidence": {"$avg": "$events.parse_data.intent.confidence"},
                "max_confidence": {"$max": "$events.parse_data.intent.confidence"},
                "min_confidence": {"$min": "$events.parse_data.intent.confidence"}}},
    {"$sort": {"average_confidence": -1}}
]

results_confidence = conversations.aggregate(pipeline_confidence)
print("Intent Confidence Stats")
print(tabulate(results_confidence, headers="keys", tablefmt="pretty"))

# User Message Length Stats
pipeline_msg_length = [
    {"$unwind": "$events"},
    {"$match": {"events.event": "user"}},
    {"$project": {"length": {"$strLenCP": "$events.text"}}},
    {"$group": {"_id": None,
                "average_length": {"$avg": "$length"},
                "max_length": {"$max": "$length"},
                "min_length": {"$min": "$length"}}}
]

results_msg_length = conversations.aggregate(pipeline_msg_length)
print("User Message Length Stats")
print(tabulate(results_msg_length, headers="keys", tablefmt="pretty"))

# Most common actions
pipeline_actions = [
    {"$unwind": "$events"},
    {"$match": {"events.event": "action", "events.name": {"$ne": "action_listen"}}},
    {"$group": {"_id": "$events.name", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]

results_actions = conversations.aggregate(pipeline_actions)
print("Most common actions")
print(tabulate(results_actions, headers="keys", tablefmt="pretty"))

# Session Duration Stats
pipeline_session_duration = [
    {"$project": {
        "session_start": {"$min": "$events.timestamp"},
        "session_end": {"$max": "$events.timestamp"}
    }},
    {"$project": {
        "session_duration": {"$subtract": ["$session_end", "$session_start"]}
    }},
    {"$group": {
        "_id": None,
        "average_duration": {"$avg": "$session_duration"},
        "max_duration": {"$max": "$session_duration"},
        "min_duration": {"$min": "$session_duration"}
    }}
]

results_session_duration = conversations.aggregate(pipeline_session_duration)
print("Session Duration Stats")
print(tabulate(results_session_duration, headers="keys", tablefmt="pretty"))

# Conversations per user
pipeline_user_conversations = [
    {"$group": {"_id": "$sender_id", "num_conversations": {"$sum": 1}}},
    {"$sort": {"num_conversations": -1}}
]

results_user_conversations = conversations.aggregate(pipeline_user_conversations)
print("Number of Conversations per User")
print(tabulate(results_user_conversations, headers="keys", tablefmt="pretty"))

client.close()
