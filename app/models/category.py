from ..database import Base
from sqlalchemy import Column, Integer,String

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    categoryName = Column(String(255), nullable=False)