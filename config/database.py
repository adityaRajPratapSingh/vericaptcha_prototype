
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import mongo_creds
from urllib.parse import quote_plus
import random
from bson import ObjectId
from datetime import datetime

uri = f"mongodb+srv://{quote_plus(mongo_creds.creds.USER)}:{quote_plus(mongo_creds.creds.PASS)}@cluster0.4cy2ale.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db=client['sentence_captcha']
collection1='sentence_w_label'
collection2='label_classes'
collection3='vericaptcha_output'

def fetch_random_document(collection_name):
    coll=db[collection_name]
    count = coll.count_documents({})
    if count !=0:
        random_index=random.randint(0, count-1)
        random_doc_cursor=coll.find().skip(random_index).limit(3)
        random_doc=list(random_doc_cursor)
        d=[dic for dic in random_doc]
        return d
    else:
        raise Exception("there are no documents in the fetch location")
    
def fetch_label_classes(collection_name):
    coll=db[collection_name]
    count = coll.count_documents({})
    if count!=0:
        docs_cursor=coll.find()
        docs=list(docs_cursor)
        return docs
    else:
        raise Exception("there are no documents in the fetch location")
    
def fetch_document(collection_name, id:str):
    coll=db[collection_name]
    doc = coll.find_one({'_id':ObjectId(id)})
    if doc:
        return doc
    else:
        raise Exception("there is no document with that id")

def find_update_upsert(collection_name, id:str, response:str):
    coll=db[collection_name]
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    dynamic_key = f'label_class_{current_time}'
    coll.find_one_and_update(
        {'_id':ObjectId(id)},
        {'$set':{'_id':ObjectId(id), dynamic_key:response}},
        upsert=True
    )