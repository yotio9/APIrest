from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from services.auth import Authservices
from schema.auth import Usercreate,Userconnect#lister_user
from db.database import db_dependency

auth_rooter = APIRouter(prefix="/auth", tags=["AUTH"])

@auth_rooter.post("/inscription/")

async def inscription(user_body: Usercreate,db:db_dependency):
    services=Authservices(db)
    return await services.inscription(user_body)
    



@auth_rooter.post("/connection/")
async def connection(body: Userconnect,db:db_dependency):
    services=Authservices(db)
    return  await services.connection(body)

#@auth_rooter.get("/lister_user/")
#def lister_user():
#    services=Authservices
#   return services.lister_user