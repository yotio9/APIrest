from datetime import date

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Text, func

from db.database import Base

class Task(Base):
    __tablename__="task"
    id=Column(Integer,primary_key=True)
    title=Column(Text)
    description=Column(Text)
    priority=Column(Text)
    completed=Column(Boolean, default=False)
    userID=Column(Integer, ForeignKey("users.id"), nullable=False)
    created=Column(Date, default=date.today, server_default=func.current_date(), nullable=False)