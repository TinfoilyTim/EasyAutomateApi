from fastapi import FastAPI
from pydantic import BaseModel, JsonValue
import os
import json

app = FastAPI()


defs = []
is_json = ".json"
is_text = ""


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
def dyn_read(name, tempj):
    with open(f"./userdeffs/{name}{tempj}", "r", encoding="utf8") as file:
        return file.read()

def dyn_write(name, tempj, indata):
    with open(f"./userdeffs/{name}{tempj}", "w", encoding="utf8") as file:
        file.write(f"os.system('{indata}')")
    






    
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
    y = json.loads(load_task_vars(payload.name, is_json))
    return {"name": payload.name, "vars_needed" : y}
    



#executes the code
@app.post("/prepare/run")
async def run(payload:send_vars):
    data = dyn_read(payload.name,is_text)

    #iterates through json variables/item names and replaces every match with its corresponding value from client payload
    for var,value in payload.vars.items():
        if f"__{var}__" in data:
            data = data.replace(f"__{var}__", value)
    exec(data)

#@app.post("/edit")
#async def edit