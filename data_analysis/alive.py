import os

from pymongo.mongo_client import MongoClient

mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")

uri = f"mongodb+srv://{mongo_user}:{mongo_password}@mycluster.xkgnpk7.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    print("Ping!")
    client.admin.command('ping')
    print("Pong!")
except Exception as e:
    print(e)
