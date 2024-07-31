from pydantic import BaseModel

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
    