from fastapi import APIRouter, HTTPException, Form
import logging
import base64
import config.text_to_img
import models.model_1
import config.database
import schemas.schema
from bson import ObjectId
import random
from typing import List, Dict
from pydantic import BaseModel, EmailStr


router = APIRouter()

@router.get("/")
async def home():
    return {"message":"received"}

@router.get('/captcha/request_captcha/{imgs_num}', response_model=List[models.model_1.captcha])
async def request_captcha(imgs_num:int)->List[Dict[str,str]]:
    req = []
    try:
        docs = config.database.fetch_random_document(config.database.collection1, imgs_num)
    except Exception as e:
        logging.error(f"Error fetching documents: {e}")
        raise HTTPException(status_code=500, detail="Error fetching documents from the database")
    
    for doc in docs:
        try:
            d = schemas.schema.individual_serialise_1(doc)
            image_bytes = config.text_to_img.get_random_image(
                "./BPtypewriteStrikethrough.ttf",
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

@router.get('/captcha/request_label_classes')
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

@router.post("/submit_request")
async def submit_request(
        name: str = Form(...),
        address: str = Form(...),
        email: EmailStr = Form(...),
        phone: str = Form(...),
        request_detail: str = Form(...),
):
    data = {
        "name": name,
        "address": address,
        "email": email,
        "phone": phone,
        "description": request_detail,
    }
    config.database.add_requested_data(data)
    config.database.send_email(data)
    return {"message": "order successfully received"}
