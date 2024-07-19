# defines CRUD operations for categories
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from  ..database import get_db
from ..models.category import Category
from ..schemas.category import CategoryBase

db_dependency = Annotated[Session, Depends(get_db)]

# reall all categories
def read_all_categories(db: db_dependency):
    categories = db.query(Category).all()
    return categories

def read_category(category_id, db: db_dependency):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category not found")
    return category

def create_category(category: CategoryBase, db: db_dependency):
    # db_check = db.query(Category).filter(Category.categoryName == category.categoryName)

    # if db_check:
    #     print("hererere")
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Category name '{category.categoryName}' is already exist.")
    
    db_category = Category(
        categoryName = category.categoryName
    )
    db.add(db_category)
    db.commit()
    return {"message": f"Category '{category.categoryName}' created successfully."}
