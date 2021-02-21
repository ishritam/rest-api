import sys
sys.path.append(".")

from fastapi import FastAPI,Request,Response,APIRouter
from typing import Optional
import uvicorn
from mongo_client import MongoDb
import config
import json
from fastapi.responses import JSONResponse
from bson import json_util
from pydantic import BaseModel, validator, ValidationError
from models.song import Song
from models.podcast import Podcast
from models.audiobook import Audiobook

app=FastAPI()	
client=MongoDb()

class Audio(BaseModel):
    audio_file_type : str
    audio_file_metadata : dict

    @validator('audio_file_type')
    def check_audio_file_type(cls,v):
        if type(v)!=str:
            raise Exception("audio_file_type should be String.")
        elif v not in ['Song','Podcast','Audiobook']:
            raise Exception("Audio type should be either of [ Song , Podcast , Audiobook ]")
        return v

    @validator('audio_file_metadata')
    def check_audio_file_metadata(cls,v):
        if type(v)!=dict:
            raise Exception("audio_file_metadata should be Dict.")
        return v


@app.post("/upload")
async def upload(request : Request):
    item_dict=await request.json()
    try:
        item=Audio(**item_dict)
        if item.audio_file_type=='Song':
            data=Song(**item.audio_file_metadata)
        elif item.audio_file_type=='Podcast':
            data=Podcast(**item.audio_file_metadata)
        elif item.audio_file_type=='Audiobook':
            data=Audiobook(**item.audio_file_metadata)

        status,error=client.execute_insert_one(item.audio_file_type,data.dict())
        if status:
            return JSONResponse(status_code=200,content={"message":"Audio added Successfully."})
        else:
            return JSONResponse(status_code=500,content={"message":error})
    except Exception as e:
        return JSONResponse(status_code=400,content={"message":str(e)})
    return  item

@app.post("/delete/{audio_type}/{audio_id}")
async def delete(audio_type , audio_id:int):
    try:
        if audio_type not in ['Song','Podcast','Audiobook']:
            raise Exception("Audio type should be either of [ Song , Podcast , Audiobook ]")

        status,error=client.execute_delete(audio_type,{"id":audio_id})
        if status:
            return JSONResponse(status_code=200,content={"message":"Audio deleted Successfully."})
        else:
            return JSONResponse(status_code=500,content={"message":error})
        return {"audio_type":audio_type,"audio_id":audio_id}
    except Exception as e:
        return JSONResponse(status_code=400,content={"message":str(e)})

@app.post("/update/{audio_type}/{audio_id}")
async def update(audio_type,audio_id:int,request : Request):
    item_dict=await request.json()
    try:
        if audio_type=='Song':
            data=Song(**item_dict)
        elif audio_type=='Podcast':
            data=Podcast(**item_dict)
        elif audio_type=='Audiobook':
            data=Audiobook(**item_dict)
        else:
            raise Exception("Audio type should be either of [ Song , Podcast , Audiobook ]")

        status,error=client.execute_update(audio_type,audio_id,data.dict())
        if status:
            return JSONResponse(status_code=200,content={"message":"Audio Updated Successfully."})
        else:
            return JSONResponse(status_code=500,content={"message":error})
    except Exception as e:
        return JSONResponse(status_code=400,content={"message":str(e)})
    return  data

@app.post('/get/{audio_type}/{audio_id:path}')
async def get(audio_type,audio_id : Optional[str]=None):
    try:
        if audio_type not in ['Song','Podcast','Audiobook']:
            raise Exception("Audio type should be either of [ Song , Podcast , Audiobook ]")
        
        if audio_id is "":
            post={}
        else:
            post={"id":audio_id}
        data=client.execute_search(audio_type,post)
        return json.loads(json_util.dumps(data))
    except Exception as e:
        return JSONResponse(status_code=400,content={"message":str(e)})





if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=2021)