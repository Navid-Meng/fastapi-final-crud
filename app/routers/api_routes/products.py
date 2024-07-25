# defines routes and endpoints for related to products

from typing import Annotated, List, Optional
from fastapi import Depends, HTTPException, Query, status, APIRouter
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session, Query as SAQuery


from app.database import get_db
from app.schemas.product import ProductBase, ProductOut
from app.models.product import Product
from app.models.category import Category
# from ...controllers.product_controller import get_products
from ...controllers import product_controller
from ..api_routes.auth import get_current_user
from ...schemas import user

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    tags={"Product"}
)

@router.get("/root", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Your api application is up and running."}

# read all products
@router.get('/api/products', status_code=status.HTTP_200_OK)
async def read_products(
        db: db_dependency,
        min_price: Optional[float] = Query(None, ge=0),
        max_price: Optional[float] = Query(None, ge=0))->Page[ProductOut]:
    products = product_controller.get_all_products(db, min_price, max_price)
    return paginate(products)

add_pagination(router)

# read one product
@router.get('/api/products/{product_id}', status_code=status.HTTP_200_OK)
async def read_product_by_id(product_id: int, db: db_dependency):
    product = product_controller.get_product_by_id(product_id=product_id, db=db)

    if product:
        return product
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id '{product_id}' not found")

# create one product
@router.post('/api/products/', status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductBase,
                         db: db_dependency,
                         current_user: user.UserBase = Depends(get_current_user)):
    created_success = product_controller.create_product(product=product, db=db)
    if created_success:
        return {"message": f"Product created successfully."}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product name '{product.productName}' is already exist.")

# bulk
@router.post('/api/products/bulk', status_code=status.HTTP_200_OK)
async def bulk_create_products(products: List[ProductBase],
                               db: db_dependency,
                               current_user: user.UserBase = Depends(get_current_user)):
    message = product_controller.bulk_create_products(products=products, db=db)
    return message

# update product
@router.put('/api/products/{product_id}', status_code=status.HTTP_200_OK)
async def update_product(product_id: int,
                         product: ProductBase,
                         db: db_dependency,
                         current_user: user.UserBase = Depends(get_current_user)):
    return product_controller.update_product(product_id, product, db)

# delete product (deactivate data)
@router.delete('/api/products/{product_id}', status_code=status.HTTP_200_OK)
async def delete_product(product_id: int,
                         db: db_dependency,
                         current_user: user.UserBase = Depends(get_current_user)):
    return product_controller.delete_product(product_id=product_id, db=db)