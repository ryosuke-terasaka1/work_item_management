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

# 会議室一覧取得
def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()

# 予約一覧取得
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()

# ユーザー登録
def create_user(db: Session, user: schemas.User):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 会議室登録
def create_room(db: Session, room: schemas.Room):
    db_room = models.Room(room_name=room.room_name, capacity=room.capacity)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

# 予約登録
def create_booking(db: Session, booking: schemas.Booking):
    db_booked = db.query(models.Booking).\
        filter(models.Booking.room_id == booking.room_id).\
        filter(models.Booking.end_datetime > booking.start_datetime).\
        filter(models.Booking.start_datetime < booking.end_datetime).\
        all()
    # 重複するデータがなければ
    if len(db_booked) == 0:
        db_booking = models.Booking(
            user_id = booking.user_id,
            room_id = booking.room_id,
            booked_num = booking.booked_num,
            start_datetime = booking.start_datetime,
            end_datetime = booking.end_datetime
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking
    else:
        raise HTTPException(status_code=404, detail="Already booked")


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
