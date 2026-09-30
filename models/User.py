from sqlalchemy import Column , String , Integer

from sqlalchemy.dialects.postgresql import ARRAY

from db.database import Base

class User (Base):
   __tablename__ = "users"
   id= Column(Integer,primary_key=True)
   nom= Column(String)
   motdpass=Column(String)
   age=Column(String)