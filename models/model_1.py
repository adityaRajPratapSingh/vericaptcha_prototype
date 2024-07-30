from pydantic import BaseModel

class Coll_1(BaseModel):
    id: str
    sentence: str
    label: int

class Coll_2(BaseModel):
    label_class: str

class Coll_3(BaseModel):
    response_text: str
    id: str
    label: int