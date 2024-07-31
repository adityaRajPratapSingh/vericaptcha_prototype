from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from urllib.parse import quote_plus

import mongo_creds

import csv

uri = f"mongodb+srv://{quote_plus(mongo_creds.creds.USER)}:{quote_plus(mongo_creds.creds.PASS)}@cluster0.4cy2ale.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
db=client['sentence_captcha']
collection=db['sentence_w_label']

with open('/home/magellan/envs/vericaptcha_prototype_mongodb/project_files/data/orignal_text_csv.csv', 'r') as file:
    csvreader=csv.reader(file)
    next(csvreader)
    next(csvreader)
    for row in csvreader:
        collection.insert_one({'sentence':row[1], 'label':row[2]})
print("DONE")