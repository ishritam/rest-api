from pydantic import BaseModel, validator, ValidationError
from datetime import datetime
from typing import List

class Audiobook(BaseModel):
    id : int
    title : str
    duration : int
    upload_time : datetime
    author : str
    narrator : str
    

    @validator('id')
    def check_id(cls,v):
        if type(v)!=int:
            raise Exception("Id should be Integer.")
        return v
    
    @validator('title')
    def check_title(cls,v):
        if type(v)!=str:
            raise Exception("Title should be String.")
        elif len(v)>10:
            raise Exception("Title should be less than 100 characters.")
        return v

    @validator('duration')
    def check_duration(cls,v):
        if type(v)!=int:
            raise Exception("Duration should be Integer.")
        elif v<0:
            raise Exception("Duration should be positive.")
        return v

    @validator('upload_time')
    def check_upload_time(cls,v):
        if type(v)!=datetime:
            raise Exception("Duration should be Integer.")
        elif v<datetime.now():
            raise Exception("upload_time should be greater than current time.")
        return v

    @validator('author')
    def check_author(cls,v):
        if type(v)!=str:
            raise Exception("author should be String.")
        elif len(v)>10:
            raise Exception("author should be less than 100 characters.")
        return v
    
    @validator('narrator')
    def check_narrator(cls,v):
        if type(v)!=str:
            raise Exception("narrator should be String.")
        elif len(v)>10:
            raise Exception("narrator should be less than 100 characters.")
        return v