from fastapi import APIRouter, HTTPException
import logging
import base64
import config.text_to_img
import models.model_1
import config.database
import schemas.schema
from bson import ObjectId
import random

router = APIRouter()

'''
@router.get('/captcha/request_captcha')
async def request_captcha():
    req=[]
    docs=config.database.fetch_random_document(config.database.collection1)
    for doc in docs:
        d=schemas.schema.individual_serialise_1(doc)
        req.append(d)
        req.append(config.text_to_img.get_random_image("/home/magellan/envs/vericaptcha_prototype_mongodb/project_files/data/BPtypewriteStrikethrough.ttf", d['sentence']))
    return req
'''

@router.get('/captcha/request_captcha')
async def request_captcha():
    req = []
    try:
        docs = config.database.fetch_random_document(config.database.collection1)
    except Exception as e:
        logging.error(f"Error fetching documents: {e}")
        raise HTTPException(status_code=500, detail="Error fetching documents from the database")
    
    for doc in docs:
        try:
            d = schemas.schema.individual_serialise_1(doc)
            req.append(d)
            
            image_bytes = config.text_to_img.get_random_image(
                "/home/magellan/envs/vericaptcha_prototype_mongodb/project_files/data/BPtypewriteStrikethrough.ttf",
                d['sentence']
            )

            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            req.append({"image": image_base64})
        except UnicodeDecodeError as e:
            logging.error(f"UnicodeDecodeError: {e} - Document: {doc}")
            raise HTTPException(status_code=500, detail="Error processing document due to encoding issue")
        except Exception as e:
            logging.error(f"Error processing document: {e}")
            raise HTTPException(status_code=500, detail="Error processing document")

    return req

@router.get('/captcha/request_label_classes')
async def request_label_classes():
    docs=config.database.fetch_label_classes(config.database.collection2)
    label_classes=[]
    for doc in docs:
        d=schemas.schema.individual_serialise_2(doc)
        label_classes.append(d['label_class'])
    return label_classes

@router.post('/captcha/response_captcha/')
async def response_captcha(responses:list[str], ids:list[str]):
    D=[]
    for id in ids:
        D.append(config.database.fetch_document(config.database.collection1, id))
    docs=config.database.fetch_label_classes(config.database.collection2)
    label_classes=[]
    for doc in docs:
        d=schemas.schema.individual_serialise_2(doc)
        label_classes.append(d['label_class'])
    for response in responses:
        if response not in label_classes:
            return False
    else:
        for id, response in zip(ids, responses):
            config.database.find_update_upsert(config.database.collection3, id, response)
        return True