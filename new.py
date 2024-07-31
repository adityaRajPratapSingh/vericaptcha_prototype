

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import config.database

uri = "mongodb+srv://magellan2409:nbLXCg85zqToP3t7@cluster0.4cy2ale.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


try:
    db = client["sentence_captcha"]
    collection = db[config.database.collection1]
    print(collection.count_documents({}))
except Exception as e:
    print(e)