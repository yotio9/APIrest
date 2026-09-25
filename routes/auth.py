from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from services.auth import Authservices
from schema.auth import Usercreate,Userconnect,lister_user


auth_rooter = APIRouter(prefix="/auth", tags=["AUTH"])

@auth_rooter.post("/inscription/")

def inscription(body: Usercreate):
    services=Authservices
    return services.inscription(body)
    



@auth_rooter.post("/connection/")
def connection(body: Userconnect):
    services=Authservices
    return  services.connection(body)

@auth_rooter.get("/lister_user/")
def lister_user():
    services=Authservices
    return services.lister_user