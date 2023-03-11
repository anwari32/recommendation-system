from database import Base
from sqlalchemy import ForeignKey, Integer, BigInteger, String, Column, DateTime, Boolean, Float


class Category(Base):
    __tablename__ = "category"

    id = Column(BigInteger, primary_key=True, index=True)
    created_date = Column(DateTime)
    name = Column(String)
    desc = Column(String)


class Item(Base):
    __tablename__ = "item"

    id = Column(BigInteger, primary_key=True, index=True)
    created_date = Column(DateTime)
    name = Column(String)
    price_per_qty = Column(Integer)
    cat_id = Column(Integer, ForeignKey("category.id"))


class Courier(Base):
    __tablename__ = "courier"

    id = Column(BigInteger, primary_key=True, index=True)
    created_date = Column(DateTime)
    name = Column(String)


class SessionRef(Base):
    __tablename__ = "session_ref"

    id = Column(BigInteger, primary_key=True, index=True)
    created_date = Column(DateTime)


class Session(Base):
    __tablename__ = "session"

    id = Column(BigInteger, primary_key=True, index=True)
    created_date = Column(DateTime)
    session_ref_id = Column(Integer, ForeignKey("session_ref.id"))
    item_id = Column(Integer, ForeignKey("item.id"))
    price = Column(Integer)
    qty = Column(Integer)
    price_per_qty = Column(Float)
    courier_id = Column(Integer, ForeignKey("courier.id"))
    insurance = Column(Boolean)

