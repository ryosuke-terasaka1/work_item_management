import datetime
from pydantic import BaseModel, Field
    
class UserCreate(BaseModel):
    username: str = Field(max_length=12)

class User(UserCreate):
    user_id: int

    class Config:
        orm_mode = True

class ItemCreate(BaseModel):
    item_name: str = Field(max_length=12)
    created_date: datetime.date
    create_num: int
    price: int


class Item(ItemCreate):
    item_id: int

    class Config:
        orm_mode = True

