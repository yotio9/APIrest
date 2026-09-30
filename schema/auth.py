from fastapi import APIRouter,HTTPException
from pydantic import BaseModel


class Usercreate(BaseModel):
    nom:str
    email:str
    age:int
    motdpass: str

class Userconnect(BaseModel):
    username:str
    motdpass:str
    