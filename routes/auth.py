from fastapi import APIRouter


auth_rooter=APIRouter(prefix="/auth", tags="AUTH")




@auth_rooter.get("/")

def home():
    return "salut la famille"



@auth_rooter.get("/mail")
def mail():
    return "tres bon mail"