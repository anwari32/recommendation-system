from pydantic import BaseModel
from typing import Union
import datetime

class CategoryBase(BaseModel):
    name: str
    desc: Union[str, None] = None


class CategoryCreate(CategoryBase):
    pass 


class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    name: str
    price_per_qty: int
    cat_id: int


class ItemCreate(ItemBase):
    pass 


class Item(ItemBase):
    id: int
    class Config:
        orm_mode = True


class CourierBase(BaseModel):
    name: str


class CourierCreate(CourierBase):
    pass


class Courier(CourierBase):
    id: int
    class Config:
        orm_mode = True


class SessionRefBase(BaseModel):
    pass


class SessionRefCreate(SessionRefBase):
    pass


class SessionRef(SessionRefBase):
    id: int
    created_date: datetime.datetime
    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    session_ref_id: int
    item_id: int
    price: int
    qty: int
    courier_id: int
    insurance: bool


class SessionCreate(SessionBase):
    pass


class Session(SessionBase):
    id: int
    created_date: datetime.datetime
    class Config:
        orm_mode = True
