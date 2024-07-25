from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# URL_DATABASE = 'mysql+pymysql://root:@localhost:3306/my_product_db'

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('MYSQL_DATABASE_URL')

if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("No SQLALCHEMY_DATABASE_URL found in environment")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base() # for ORM purposes

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()