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
    