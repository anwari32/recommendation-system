from sqlalchemy.orm import Session
from datetime import datetime

import models, schemas
import numpy as np

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(
        name=item.name, 
        price_per_qty=item.price_per_qty, 
        cat_id=item.cat_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_item_by_name(db: Session, item_name: str):
    return db.query(models.Item).filter(models.Item.name == item_name).first()

def get_item_by_cat_id(db: Session, cat_id: int):
    return db.query(models.Item).filter(models.item.cat_id == cat_id).first()

def get_session_by_item_cat_id(db: Session, item_cat_id: int):
    db_items = db.query(models.Item).filter(models.Item.cat_id == item_cat_id)
    db_item_ids = [_item.id for _item in db_items]
    db_item_ids = np.unique(db_item_ids).tolist()
    # print(f"item ids {db_item_ids}")
    return db.query(models.Session).filter(models.Session.item_id.in_(db_item_ids)).all()

def get_session(db: Session, skip=0, limit=100):
    return db.query(models.Session).offset(skip).limit(limit).all()