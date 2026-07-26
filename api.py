from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import test


app = FastAPI()

class DownloadRequest(BaseModel):
    path:str
    url:str
    zip: bool
    format: str

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
    

