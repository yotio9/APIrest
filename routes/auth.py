from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from services.auth import Authservices
from schema.auth import Usercreate,Userconnect,Usertask#lister_user
from db.database import db_dependency
from core.security import get_current_user_id


auth_rooter = APIRouter(prefix="/auth", tags=["AUTH"])

@auth_rooter.post("/inscription/")
async def inscription(user_body: Usercreate,db:db_dependency):
    print(db)
    services=Authservices(db)
    return await services.inscription(user_body)
    

@auth_rooter.post("/Give_task/")
async def Give_task(
    body: Usertask,
    db: db_dependency,
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    services=Authservices(db)
    return await services.Give_tasks(body, user_id)


@auth_rooter.get("/Get_tasks/")
async def Get_tasks(
    db: db_dependency,
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    services=Authservices(db)
    return await services.Get_tasks(user_id)


@auth_rooter.post("/connection/")
async def connection(
    body: Userconnect,
    db: db_dependency,
    request: Request,
    response: Response,
):
    services=Authservices(db)
    result = await services.connection(body)
    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=request.url.scheme == "https",
        samesite="lax",
        max_age=1800,
        path="/",
    )
    return result



@auth_rooter.get("/list_all_user/")
async def list_all_user(db:db_dependency):
    services=Authservices(db)
    return await services.list_all_user()
