from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'mysql+pymysql://root:@localhost:3306/my_product_db'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base() # for ORM purposes

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()