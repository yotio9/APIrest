from pydantic import BaseModel
from fastapi import APIRouter,HTTPException,status,Query
from sqlalchemy import select
from core.security import create_access_token
from schema.auth import Usercreate,Userconnect,Usertask,Uptask,Droptask,filtertask
from db.database import db_dependency, AsyncSession
from models.User import User
from models.Task import Task
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
      username_field=user_body.email# on recuperer les donnees 
      motdpass_field=user_body.motdpass
      smt=await self.db.execute(
         select(User).where(User.email == username_field)#on ecrit la requete
      )
      user = smt.scalar_one_or_none()
      if not user or not password_context.verify(motdpass_field, user.motdpass) :
         raise HTTPException(detail="motdpass ou email incorrect",status_code=status.HTTP_401_UNAUTHORIZED)
   
      return {
         "message": "Connexion réussie",
         "access_token": create_access_token(str(user.id)),
         "token_type": "bearer",
      }

   async def list_all_user(self):
    resultat = await self.db.execute(
        select(User).where(User.age == "17")
    )

    users = resultat.scalars().first()

    return users

   async def Give_tasks(self, user_body: Usertask, user_id: int):
      new_task=Task(
         title=user_body.title,
         description=user_body.description,
         priority=user_body.priority,
         userID=user_id,
               )
      self.db.add(new_task)
      await self.db.commit()
      await self.db.refresh(new_task)
      return new_task

   async def Get_tasks(self, user_id: int):
      resultat =await self.db.execute(
         select(Task).where(Task.userID == user_id)
      )
      tasks=resultat.scalars().all()

      return tasks
   
   
   async def Up_tasks(self,body:Uptask, user_id:int):
      resultat = await self.db.execute(
         select(Task).where(
            Task.id == body.id_task,
            Task.userID == user_id,
         )
      )
      task = resultat.scalar_one_or_none()
      if task is None:
         raise HTTPException(
            detail="Tâche introuvable",
            status_code=status.HTTP_404_NOT_FOUND,
         )

      task.title = body.new_task
      await self.db.commit()
      await self.db.refresh(task)
      return task

   async def Drop_task(self,body:Droptask,user_id:int):
      resultat = await self.db.execute(
         select(Task).where(
            Task.id == body.id_task,
            Task.userID == user_id,
         )
      )
      task = resultat.scalar_one_or_none()
      if task is None:
         raise HTTPException(
            detail="Tâche introuvable",
            status_code=status.HTTP_404_NOT_FOUND,
         )

      await self.db.delete(task)
      await self.db.commit()
      return {"message": "Tâche supprimée"}


   async def Task_completed(self,body:filtertask ,user_id:int):
      resultat = await self.db.execute(
         select(Task).where(
                Task.userID == user_id,
                Task.completed == body.completed_state,
         )
      )
      tasks = resultat.scalars().all()
      return tasks

   async def priority_filter(self,body:filtertask ,user_id:int):
      resultat = await self.db.execute(
         select(Task).where(
                Task.userID == user_id,
                Task.priority == body.priority_search,
         )
      )
      tasks = resultat.scalars().all()
      return tasks
