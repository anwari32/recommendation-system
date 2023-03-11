from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_config import db_user, db_password, db_host, db_name

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{dn_host}/{db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


