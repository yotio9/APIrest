from fastapi import FastAPI
from routes.auth import auth_rooter

app=FastAPI()
app.include_router(auth_rooter)