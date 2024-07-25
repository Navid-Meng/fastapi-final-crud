# defines schemas for products
from pydantic import BaseModel
from typing import Annotated, List, Optional

class ProductBase(BaseModel):
    productName: str
    price: float
    stockQty: int
    categoryId: int
    is_active: Optional[bool] = True
    productCode: str
    
class ProductOut(BaseModel):
    id: int
    productName: str
    price: float
    stockQty: int
    categoryId: int
    is_active: Optional[bool] = True
    productCode: str