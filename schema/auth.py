from fastapi import APIRouter,HTTPException
from pydantic import BaseModel


class Usercreate(BaseModel):
    nom:str
    email:str
    age:str
    motdpass: str

class Userconnect(BaseModel):
    email:str
    motdpass:str

class Usertask(BaseModel):
    title:str
    description:str
    priority:str  

class Uptask(BaseModel):
    id_task:int
    new_task:str

class Droptask(BaseModel):
    id_task:int

class filtertask(BaseModel):
    id_task:int
    priority_search:str
    completed_state:bool
