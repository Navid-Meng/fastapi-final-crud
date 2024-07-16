from fastapi import FastAPI, status, Depends, HTTPException, Request, Form
import models
from database import engine, SessionLocal
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated, List
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)

class ProductBase(BaseModel):
    productName: str
    price: float
    stockQty: int
    categoryId: int
    
class CategoryBase(BaseModel):
    categoryName: str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
db_dependency = Annotated[Session, Depends(get_db)]

# endpoints for api clients #

# read all products
@app.get('/api/products', status_code=status.HTTP_200_OK)
async def read_products(db: db_dependency):
    products = db.query(models.Product).all()
    return products

# read all categories
@app.get('/api/categories', status_code=status.HTTP_200_OK)
async def read_categories(db: db_dependency):
    categories = db.query(models.Category).all()
    return categories

@app.get('/api/products/{product_id}', status_code=status.HTTP_200_OK)
async def read_products(product_id: int, db: db_dependency):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get('/api/categories/{category_id}', status_code=status.HTTP_200_OK)
async def read_categories(category_id: int, db: db_dependency):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.post('/api/products/', status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductBase, db: db_dependency):
    db_product = models.Product(productName=product.productName, price=product.price, stockQty=product.stockQty, categoryId=product.categoryId)
    db.add(db_product)
    db.commit()
    return {"message": f"Product created successfully."}

# bulk 
@app.post('/api/products/bulk', status_code=status.HTTP_200_OK)
async def bulk_create_product(products: List[ProductBase], db: db_dependency):
    try:
        db_products = [
            models.Product(productName=product.productName, price=product.price, stockQty=product.stockQty, categoryId=product.categoryId)
            for product in products
        ]
        db.add_all(db_products)
        db.commit()
        return {"message": f"Products created successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=(e))
    
@app.post('/api/categories/', status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryBase, db: db_dependency):
    db_category = models.Category(categoryName=category.categoryName)
    db.add(db_category)
    db.commit()
    return {"message": f"Category created successfully."}
    
@app.put('/api/categories/{category_id}', status_code=status.HTTP_200_OK)
async def update_category(db: db_dependency, category_id: int, new_category_name: str):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(f"Category with id {category_id} not found")
    db_category.categoryName = new_category_name
    db.add(db_category)
    db.commit()
    return {"message": f"Category with id {category_id} updated successfully"}

@app.put('/api/products/{product_id}', status_code=status.HTTP_200_OK)
async def update_product(db: db_dependency, product_id: int, product: ProductBase):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(f"Product with id {product_id} not found")
    db_product.productName = product.productName
    db_product.price = product.price
    db_product.stockQty = product.stockQty
    db_product.categoryId = product.categoryId
    db.add(db_product)
    db.commit()
    return {"message": f"Category with id {product_id} updated successfully"}

@app.delete("/api/products/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, db: db_dependency):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(f"Product with id {product_id} not found")
    db.delete(db_product)
    db.commit()
    return {"message": f"Product with id {product_id} deleted successfully."}

# endpoints for HTMLResponse

@app.get('/products/read', response_class=HTMLResponse)
async def read_product_html(request: Request, db: db_dependency):
    products = db.query(models.Product).all()
    return templates.TemplateResponse("display.html", {"request": request, "products": products})

@app.get('/products/create', response_class=HTMLResponse)
async def create_product_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.get('/products/update/{product_id}', response_class=HTMLResponse)
async def update_product_form(product_id: int,request: Request, db: db_dependency):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    return templates.TemplateResponse("update.html", {"request": request, "product": product})