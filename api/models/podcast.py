from pydantic import BaseModel, validator, ValidationError
from datetime import datetime
from typing import List

class Podcast(BaseModel):
    id : int
    name : str
    duration : int
    upload_time : datetime
    host : str
    participants : List

    @validator('id')
    def check_id(cls,v):
        if type(v)!=int:
            raise Exception("Id should be Integer.")
        return v
    
    @validator('name')
    def check_name(cls,v):
        if type(v)!=str:
            raise Exception("Name should be String.")
        elif len(v)>10:
            raise Exception("Name should be less than 100 characters.")
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

    @validator('host')
    def check_host(cls,v):
        if type(v)!=str:
            raise Exception("Host should be String.")
        elif len(v)>10:
            raise Exception("Host should be less than 100 characters.")
        return v
    
    @validator('participants')
    def check_participants(cls,v):
        for item in v:
            if type(item)!=str:
                raise Exception("Participant should be String.")
            elif len(item)>10:
                raise Exception("Participant should be less than 100 characters.")
        if len(v)>10:
            raise Exception("Total participants should not be greater than 10.")
        return v