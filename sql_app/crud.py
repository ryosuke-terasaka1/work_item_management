from venv import create
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas
from fastapi import HTTPException
from typing import Union, Optional, Dict, Any
import datetime

def _get_by_id(self, id: int) -> Optional[models.User]:
    get_user_model = (
        self.db.query(models.User).filter(models.User.user_id == id).first()
    )
    if not get_user_model:
        return None
    return get_user_model


# ユーザー一覧取得
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# 商品一覧取得
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


# ユーザー登録
def create_user(db: Session, user: schemas.User):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 商品登録
def create_item(db: Session, item: schemas.Item):
    db_item = models.Item(item_name=item.item_name, created_date=item.created_date)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_user(
    db: Session, id: int, obj_in: Union[schemas.User, Dict[str, Any]]
) -> Optional[schemas.User]:
    get_user_model = _get_by_id(id)
    if not get_user_model:
        raise HTTPException(status_code=404, detail="指定されたユーザーは存在しません")

    for var, value in vars(obj_in).items():
        setattr(get_user_model, var, value) if value else None

    get_user_model.updated_at = datetime.utcnow()
    db.add(get_user_model)
    db.commit()
    db.refresh(get_user_model)
    return get_user_model

def delete(db:Session, id: int) -> Optional[schemas.User]:
    delete_user_model = models.User.delete().where(models.User.user_id == id)
    if not delete_user_model:
        raise HTTPException(status_code=404, detail="指定されたユーザーは存在しないか，既に削除されています")
    delete_user_schemas = schemas.User.from_orm(delete_user_model)
    db.delete_user_model()
    return delete_user_schemas
