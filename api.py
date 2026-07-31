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

class send_vars(BaseModel):
    name:str
    vars:JsonValue

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
    

#executes the code
@app.post("/prepare/run")
async def runtest(payload:send_vars):
    with open(f"userdeffs/{payload.name}","r", encoding="utf8") as file:
        data = file.read()
        #iterates through json variables/item names and replaces every match with its corresponding value from client payload
        for var,value in payload.vars.items():
            if f"__{var}__" in data:
                data = data.replace(f"__{var}__", value)
        exec(data)

