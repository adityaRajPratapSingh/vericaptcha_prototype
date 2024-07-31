
from fastapi import HTTPException
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import errors
import models.model_1
import mongo_creds
from urllib.parse import quote_plus
import random
from bson import ObjectId
from datetime import datetime
from typing import List, Dict
import schemas
import schemas.schema
import smtplib
import models

# uri for the prototype Cluster0
uri = f"mongodb+srv://{quote_plus(mongo_creds.creds.USER)}:{quote_plus(mongo_creds.creds.PASS)}@cluster0.4cy2ale.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
s = smtplib.SMTP("smtp.gmail.com", 587)

# connect to the prototype databse in Cluster0
db=client['sentence_captcha']

# collections in the prototype database
collection1='sentence_w_label'
collection2='label_classes'
collection3='vericaptcha_output'
collection4='user_request_data'

def fetch_random_document(collection_name:str, imgs_num:int)->List[Dict[str,str]]:
    try:
        coll=db[collection_name]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'there is no collection by the name {collection_name}')
    count = coll.count_documents({})
    if count !=0:
        random_index=random.randint(0, count-1)
        random_doc_cursor=coll.find().skip(random_index).limit(imgs_num)
        random_doc_list=list(random_doc_cursor)

        for doc in random_doc_list:
            serialised_doc=schemas.schema.individual_serialise_1(doc)
            if len(serialised_doc['sentence'])>175:
                return fetch_random_document(collection_name, imgs_num)
        return random_doc_list
    else:
        raise HTTPException(status_code=500, detail="there are no documents in the fetch location")
    
def fetch_label_classes(collection_name:str)->List[str]:
    try:
        coll=db[collection_name]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'there is no collection by the name {collection_name}')
    count = coll.count_documents({})
    if count!=0:
        docs_cursor=coll.find()
        docs_list=list(docs_cursor)
        return docs_list
    else:
        raise HTTPException(status_code=500, detail="there are no documents in the fetch location")
    
def fetch_document(collection_name:str, id:str)->Dict[str,str]:
    try:
        coll=db[collection_name]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'there is no collection by the name {collection_name}')
    doc = coll.find_one({'_id':ObjectId(id)})
    if doc:
        return doc
    else:
        raise HTTPException(status_code=500, detail="there is no document with that id")

def find_update_upsert(collection_name:str, sentence_id:str, response_text:str)->None:
    try:
        coll=db[collection_name]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'there is no collection by the name {collection_name}')
    
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    dynamic_key = f'label_class_{current_time}'

    try:
        coll.find_one_and_update(
            {'_id':ObjectId(sentence_id)},
            {'$set':{'_id':ObjectId(sentence_id), dynamic_key:response_text}},
            upsert=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    

def send_email(data: models.model_1.RequestedData):
    s.connect("smtp.gmail.com", 587)
    s.starttls()
    s.login("riyanshi98765riyanshi4321@gmail.com", "hchcecktogakpbwh")
    message = f"""
        Subject: Custom Dataset Request Received ( : 

        Hey there,

        Hope you are doing good.

        We have received your custom dataset request and we will get back to you as soon as it gets ready.
        
        kya halla hai re!!!
        """
    s.sendmail("riyanshi98765riyanshi4321@gmail.com", data["email"], message)
    s.quit()

def add_requested_data(data: models.model_1.RequestedData):
    try:
        collection = db[collection4]
        id = collection.insert_one(data)
    except errors.PyMongoError as e:
        raise Exception(f'{e}')