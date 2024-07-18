from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    productName = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    stockQty = Column(Integer, nullable=False)
    categoryId = Column(Integer, ForeignKey('categories.id'), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    category = relationship('Category', backref='products')
    
    

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    categoryName = Column(String(255), nullable=False)
