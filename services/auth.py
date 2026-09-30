from pydantic import BaseModel
from fastapi import APIRouter,HTTPException
from schema.auth import Usercreate,Userconnect
from db.database import db_dependency, AsyncSession
from models.User import User
from pwdlib import PasswordHash

password_context = PasswordHash.recommended()


class Authservices:
   def __init__(self, db: AsyncSession =db_dependency):
     self.db=db  

   async def inscription(self,user_body:Usercreate):
      user_body.motdpass = password_context.hash(user_body.motdpass)
      new_user= User(nom=user_body.nom,email=user_body.email,age=user_body.age,motdpass=user_body.motdpass)
      self.db.add(new_user)
      self.db.commit()
      self.db.refresh(new_user)
      

   async def connection(user:Userconnect):
    pass 