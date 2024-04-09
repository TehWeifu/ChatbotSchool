from pymongo.mongo_client import MongoClient

from cfg.mongo_cfg import *

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@mycluster.xkgnpk7.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    print("Ping!")
    client.admin.command('ping')
    print("Pong!")
except Exception as e:
    print(e)
