from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import test

defs = []

app = FastAPI()

class DownloadRequest(BaseModel):
    path:str
    url:str
    zip: bool
    format: str

class create_vars(BaseModel):
    name:str
    bash:bool
    python:bool
    code:str




@app.post("/send")
def read_root(payload: DownloadRequest):
    path = payload.path
    url = payload.url
    if payload.zip:
        os.system('rm -rf temp.zip')
        os.system(f'curl -Lo "{path}temp.zip" {url} && UNZIP_DISABLE_ZIPBOMB_DETECTION=TRUE unzip {path}temp.zip -d {path} && rm {path}temp.zip')
        return {"status": "recieved", "data" : payload}
    else:
        print(path,url,zip,format)
        return {"status": "recieved", "data" : payload}
    
#test to create function via api
@app.post("/create")
def create(payload: create_vars):
    with open(f"userdeffs/{payload.name}.txt", "w", encoding="utf8") as file:
       file.write(f"os.system('{payload.code}')")