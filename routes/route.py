from fastapi import APIRouter, HTTPException
import logging
import base64
import config.text_to_img
import models.model_1
import config.database
import schemas.schema
from bson import ObjectId
import random
from typing import List, Dict
from pydantic import BaseModel

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

@router.get('/captcha/request_captcha', response_model=List[models.model_1.captcha])
async def request_captcha()->List[Dict[str,str]]:
    req = []
    try:
        docs = config.database.fetch_random_document(config.database.collection1)
    except Exception as e:
        logging.error(f"Error fetching documents: {e}")
        raise HTTPException(status_code=500, detail="Error fetching documents from the database")
    
    for doc in docs:
        try:
            d = schemas.schema.individual_serialise_1(doc)
            image_bytes = config.text_to_img.get_random_image(
                "/home/magellan/envs/vericaptcha_prototype_mongodb/project_files/data/BPtypewriteStrikethrough.ttf",
                d['sentence']
            )
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            d['image']=image_base64
            req.append(d)
        except UnicodeDecodeError as e:
            logging.error(f"UnicodeDecodeError: {e} - Document: {doc}")
            raise HTTPException(status_code=500, detail="Error processing document due to encoding issue")
        except Exception as e:
            logging.error(f"Error processing document: {e}")
            raise HTTPException(status_code=500, detail="Error processing document")

    return req

@router.get('/captcha/request_label_classes', response_model=List[models.model_1.labels])
async def request_label_classes()->List[str]:
    try:
        docs = config.database.fetch_label_classes(config.database.collection2)
    except Exception as e:
        logging.error(f"Error fetching documents: {e}")
        raise HTTPException(status_code=500, detail="Error fetching documents from the database")
    
    label_classes=[]
    for doc in docs:
        try:
            d=schemas.schema.individual_serialise_2(doc)
            label_classes.append(d['label_class'])
        except UnicodeDecodeError as e:
            logging.error(f"UnicodeDecodeError: {e} - Document: {doc}")
            raise HTTPException(status_code=500, detail="Error processing document due to encoding issue")
        except Exception as e:
            logging.error(f"Error processing document: {e}")
            raise HTTPException(status_code=500, detail="Error processing document")
    return label_classes

# the type of the request body is like List[List[student_id, response_text]]

@router.post('/captcha/response_captcha/', response_model=bool)
async def response_captcha(responses:List[List[str]])->bool:
    try:
        docs = config.database.fetch_label_classes(config.database.collection2)
    except Exception as e:
        logging.error(f"Error fetching documents: {e}")
        raise HTTPException(status_code=500, detail="Error fetching documents from the database")
    
    label_classes=[]
    for doc in docs:
        try:
            d=schemas.schema.individual_serialise_2(doc)
            label_classes.append(d['label_class'])
        except UnicodeDecodeError as e:
            logging.error(f"UnicodeDecodeError: {e} - Document: {doc}")
            raise HTTPException(status_code=500, detail="Error processing document due to encoding issue")
        except Exception as e:
            logging.error(f"Error processing document: {e}")
            raise HTTPException(status_code=500, detail="Error processing document")
    
    for response in responses:
        if response[1] not in label_classes:
            return False
    else:
        for response in responses:
            config.database.find_update_upsert(config.database.collection3,response[0],response[1])
        return True