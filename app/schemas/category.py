# defines schemas for category
from pydantic import BaseModel

class CategoryBase(BaseModel):
    categoryName: str
    