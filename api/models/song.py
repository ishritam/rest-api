from pydantic import BaseModel, validator, ValidationError
from datetime import datetime

class Song(BaseModel):
    id : int
    name : str
    duration : int
    upload_time : datetime

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