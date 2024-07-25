from sqlalchemy import Column, Integer, String
from ..database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    