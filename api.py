from fastapi import FastAPI, Request
from pydantic import BaseModel, JsonValue
import os
import json

defs = []

app = FastAPI()


#define json payloads for post requests
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
    vars:JsonValue

class retrieve_vars(BaseModel):
    name:str


#load user created tasks into defs list by reading file names
def load_defs():
    global defs
    defs = []
    for (root,dirs,files) in os.walk("./userdeffs"):
        for file in files:
            if file.endswith(".json"):
                continue
            else:
                defs.append(file)

#read json file for corresponding task
def load_task_vars(name):
    with open(f"./userdeffs/{name}.json", "r", encoding="utf8") as file:
            return file.read()



@app.post("/send")
async def read_root(payload: DownloadRequest):
    path = payload.path
    url = payload.url
    if payload.zip:
        os.system('rm -rf temp.zip')
        os.system(f'curl -Lo "{path}temp.zip" {url} && UNZIP_DISABLE_ZIPBOMB_DETECTION=TRUE unzip {path}temp.zip -d {path} && rm {path}temp.zip')
        return {"status": "recieved", "data" : payload}
    else:
        print(path,url,zip,format)
        return {"status": "recieved", "data" : payload}
    
#test to create tasks via api
@app.post("/create")
async def create(payload: create_vars):
    if payload.bash:
        with open(f"userdeffs/{payload.name}", "w", encoding="utf8") as file:
            file.write(f"os.system('{payload.code}')") #user inputted bash script
        with open (f"userdeffs/{payload.name}.json", "w", encoding="utf8") as file:
            file.write(json.dumps(payload.vars))
            load_defs()             #reload user created tasks
            return {"vars": payload.vars}

#initial load of tasks upon app launch
@app.get("/")
async def load():
    load_defs()
    return {"defs": defs }

#run user created task next on the list
@app.post("/prepare")
async def prepare(payload:retrieve_vars):
    y = json.loads(load_task_vars(payload.name))
    return {"name": payload.name, "vars_needed" : y}
    


