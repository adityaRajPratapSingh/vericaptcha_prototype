import base64
import logging
import smtplib
from typing import List, Dict
from urllib.parse import quote_plus

from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient, errors

import config.database
import config.text_to_img
import models.model_1
import schemas.schema

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
async def request_captcha() -> List[Dict[str, str]]:
    req = []
    try:
        docs = config.database.fetch_random_document(config.database.collection1)
        logging.error(docs)
    except Exception as e:
        logging.error(f"Error fetching documents: {e}")
        raise HTTPException(status_code=500, detail="Error fetching documents from the database")

    for doc in docs:
        try:
            logging.error(doc)
            d = schemas.schema.individual_serialise_1(doc)
            logging.error(d)
            # image_bytes = config.text_to_img.get_random_image(
            #     "../data/BPtypewriteStrikethrough.ttf",
            #     d['sentence']
            # )
            # image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            # d['image'] = image_base64
            req.append(d)
        except UnicodeDecodeError as e:
            logging.error(f"UnicodeDecodeError: {e} - Document: {doc}")
            raise HTTPException(status_code=500, detail="Error processing document due to encoding issue")
        except Exception as e:
            logging.error(f"Error processing document: {e}")
            raise HTTPException(status_code=500, detail="Error processing document")

    return req


@router.get('/captcha/request_label_classes', response_model=List[models.model_1.labels])
async def request_label_classes() -> List[str]:
    try:
        docs = config.database.fetch_label_classes(config.database.collection2)
    except Exception as e:
        logging.error(f"Error fetching documents: {e}")
        raise HTTPException(status_code=500, detail="Error fetching documents from the database")

    label_classes = []
    for doc in docs:
        try:
            d = schemas.schema.individual_serialise_2(doc)
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
async def response_captcha(responses: List[List[str]]) -> bool:
    try:
        docs = config.database.fetch_label_classes(config.database.collection2)
    except Exception as e:
        logging.error(f"Error fetching documents: {e}")
        raise HTTPException(status_code=500, detail="Error fetching documents from the database")

    label_classes = []
    for doc in docs:
        try:
            d = schemas.schema.individual_serialise_2(doc)
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
            config.database.find_update_upsert(config.database.collection3, response[0], response[1])
        return True

'''

class RequestedData(BaseModel):
    name: str
    email: EmailStr
    requested_detail: str
    phone_no: int

s = smtplib.SMTP("smtp.gmail.com", 587)


# URL encode the username and password
username = quote_plus("AbhinavSingh")
password = quote_plus("Singhabhii@890")

uri = f"mongodb+srv://{username}:{password}@datasetrequests.4refzon.mongodb.net/"
client = MongoClient(uri)
database = client["request_database"]

logging.basicConfig(level=logging.INFO)
info_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)
error_logger = logging.getLogger(__name__)


@router.get("/")
def home():
    info_logger.info("home endpoint accessed")
    return {"message": "received"}


@router.post("/submit_request")
def submit_request(
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
    info_logger.info("submit-request endpoint accessed")
    add_requested_data(data)
    send_email(data)
    return {"message": "order successfully received"}


def send_email(data: RequestedData):
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


def add_requested_data(data: RequestedData):
    try:
        collection = database["request_collections"]
        id = collection.insert_one(data)
        info_logger.info(f"data added successfully with id -> {id.inserted_id}")
    except errors.PyMongoError as e:
        error_logger.error(f"An error occurred: {e}")

'''