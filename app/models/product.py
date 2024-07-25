from sqlalchemy import Column, Integer, Float, ForeignKey, Boolean, String, CheckConstraint, event
from ..database import Base
from sqlalchemy.orm import relationship
from fastapi import HTTPException, status

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    productName = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    stockQty = Column(Integer, nullable=False)
    categoryId = Column(Integer, ForeignKey('categories.id'), nullable=False)
    productCode = Column(String(5), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    __table_args__ = (
        CheckConstraint('length(productCode) = 5', name='product_code_length_check'),
    )
    
    category = relationship('Category', backref='products')
    
def validate_product_code(mapper, connection, target):
    if len(target.productCode) != 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product code must be 5 characters long.")

event.listen(Product, 'before_insert', validate_product_code)
event.listen(Product, 'before_update', validate_product_code)