import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
load_dotenv()

class Base(DeclarativeBase):
    pass

SQLALCHEMY_DATABASE_URL= os.environ["DATABASE_URL"]
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()