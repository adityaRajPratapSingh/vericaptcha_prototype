from pydantic import BaseModel, EmailStr

class captcha(BaseModel):
    id: str
    sentence: str
    label: int
    image: str

class labels(BaseModel):
    label_class: str

class Coll_3(BaseModel):
    response_text: str
    id: str
    label: int

class responses(BaseModel):
        sentence_id:str
        response_text:str
    
class RequestedData(BaseModel):
    name: str
    email: EmailStr
    requested_detail: str
    phone_no: int