import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
import os
DATABASE_URL = os.getenv("DATABASE_URL")


CHEMIN_DATA="postgresql://postgres:postgres@localhost:5000/api_db"

engine = create_engine(CHEMIN_DATA, echo=True)

sessionlocal=sessionmaker(bind=engine)

Base=declarative_base()


