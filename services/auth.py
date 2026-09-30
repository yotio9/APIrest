from pydantic import BaseModel
from fastapi import APIRouter,HTTPException
from schema.auth import Usercreate,Userconnect

listuser: list[Usercreate] = []
class Authservices :
 def inscription(user:Usercreate):
    for u in listuser:
            if u["email"]==user.email:
                raise HTTPException(409,"utlilisateur existe deja")
    
    listuser.append(user)
    return user


 def connection(user:Userconnect):
    for u in listuser:
            if u.username == user.username and u.motdpass == user.motdpass:
                return user
    raise HTTPException(401, "nom d'utilisateur ou mot de passe incorrect")
 
 def lister()