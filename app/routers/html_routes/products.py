# # endpoints for HTMLResponse
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from ...database import get_db
from ...models.category import Category
from ...models.product import Product
from sqlalchemy.orm import Session

router = APIRouter(
    tags={"HTML api router for product"}
)

templates = Jinja2Templates(directory="app/templates")

@router.get('/products/read', response_class=HTMLResponse)
async def read_product_html(request: Request):
    return templates.TemplateResponse("display.html", {"request": request})

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/products/create', response_class=HTMLResponse)
async def create_product_form(request: Request, db: db_dependency):
    categories = db.query(Category).all()
    return templates.TemplateResponse("create.html", {"request": request, "categories": categories})

@router.get('/products/update/{product_id}', response_class=HTMLResponse)
async def update_product_form(product_id: int,request: Request, db: db_dependency):
    product = db.query(Product).filter(Product.id == product_id).first()
    categories = db.query(Category).all()
    current_category = db.query(Category).filter(Category.id == product.categoryId).first()
    return templates.TemplateResponse("update.html", {"request": request, "product": product, "categories": categories, "current_category": current_category})