# defines routes and endpoints related to categories
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter, HTTPException
from ...database import get_db
from ...models.category import Category
from app.schemas.category import CategoryBase
from ...controllers import category_controller

db_dependency = Annotated[Session, Depends(get_db)]

'''
    - db_dependency is of type 'Session'
    - the value of Session will be obtained by executing get_db
    - Depends(get_db), ensuring that before any endpoints used the db_dependency, it will execute the get_db first
'''

router  = APIRouter(
    tags={"Category"}
)

# read all categories
@router.get('/api/categories', status_code=status.HTTP_200_OK)
async def read_all_categories(db: db_dependency):
    return category_controller.read_all_categories(db=db)

# read one category
@router.get('/api/categories/{category_id}', status_code=status.HTTP_200_OK)
async def read_category(category_id: int, db: db_dependency):
    return category_controller.read_category(db=db, category_id=category_id)

# create a new category
# @router.post('/api/categories/', status_code=status.HTTP_201_CREATED)
# async def create_category(category: CategoryBase, db: db_dependency):
#     db_category = Category(categoryName=category.categoryName)
#     db.add(db_category)
#     db.commit()
#     return {"message": f"Category created successfully."}

# create a new category
@router.post('/api/categories', status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryBase, db: db_dependency):
    return category_controller.create_category(db=db, category=category)

