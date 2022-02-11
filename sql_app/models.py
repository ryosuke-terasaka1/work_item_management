from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, true
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.sqltypes import Date
from .database import Base

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, unique=True, index=True)
    created_date = Column(DateTime, nullable=true)
    create_num = Column(Integer, nullable=true)
    price = Column(Integer, nullable=true)
