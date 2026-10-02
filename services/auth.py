from pydantic import BaseModel
from fastapi import APIRouter,HTTPException,status,Query
from sqlalchemy import select
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
      new_user= User(
         nom=user_body.nom,
         email=user_body.email,
         age=user_body.age,
         motdpass=user_body.motdpass)
      self.db.add(new_user)
      await self.db.commit()
      await self.db.refresh(new_user)
      return {"message": "Utilisateur créé"}
      

   async def connection(self, user_body:Userconnect):
      username_field=user_body.email
      motdpass_field=user_body.motdpass
      smt=await self.db.execute(
         select(User).where(User.email == username_field)
      )
      user = smt.scalar_one_or_none()
      if not user or not password_context.verify(motdpass_field, user.motdpass) :
         raise HTTPException(detail="motdpass ou email incorrect",status_code=status.HTTP_401_UNAUTHORIZED)
   
      return user

   async def list_all_user(self):
    resultat = await self.db.execute(
        select(User).where(User.age == "17")
    )

    users = resultat.scalars().first()

    return users