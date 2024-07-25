# defines CRUD operations for products
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, Query, HTTPException, status
from app.database import get_db
from fastapi_pagination import Page
from ..schemas.product import ProductOut, ProductBase
from ..models.product import Product
from ..models.category import Category

db_dependency = Annotated[Session, Depends(get_db)]

def get_all_products(
    db: db_dependency,
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0))->Page[ProductOut]:
    
    query = db.query(Product).filter(Product.is_active == True)
    if min_price is not None and max_price is not None:
        query = query.filter(Product.price >= min_price, Product.price <= max_price)
    elif min_price is not None:
        query = query.filter(Product.price >= min_price)
    elif max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    products = query.all()
    return products

def get_product_by_id(product_id: int, db: db_dependency):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        if not product.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id '{product_id} not found'")
        category = db.query(Category.categoryName).filter(Category.id == product.categoryId).scalar()
        product_data = {
            "id": product_id,
            "productName": product.productName,
            "price": product.price,
            "stockQty": product.stockQty,
            "categoryName": category
        }
        return product_data

def create_product(product: ProductBase, db: db_dependency):
    print("functon create product called")
    active_product = db.query(Product).filter(
        Product.productName == product.productName,
        Product.is_active == True
        ).first()
    
    if active_product:
        print(f"Active product found with name : {active_product.productName}")
        return False
    
    inactive_product = db.query(Product).filter(
        Product.productName == product.productName,
        Product.is_active == False
        )
    # if db_check:
    #     print("inside checking")
    #     print(db_check.id)
    #     if db_check.is_active:
    #         print(db_check.is_active)
    #         return False
    db_product = Product(
        productName = product.productName,
        price = product.price,
        stockQty = product.stockQty,
        categoryId = product.categoryId,
        productCode = product.productCode
    )

    db.add(db_product)
    db.commit()
    return True

def bulk_create_products(products: List[ProductBase], db: db_dependency):
    created_products = []
    for i in range(len(products)-1):
        if products[i].productName == products[i+1].productName:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product List must not contain the same ProductName.")
    for product in products:
        db_check = db.query(Product).filter(Product.productName == product.productName).first()
        if db_check and db_check.is_active:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product name '{product.productName}' already exists")
        db_product = Product(
            productName = product.productName,
            price = product.price,
            stockQty = product.stockQty,
            categoryId = product.categoryId,
            is_active = product.is_active
        )
        db.add(db_product)
        created_products.append(db_product)
    db.commit()
    return {"message": f"{len(created_products)} products created successfully."}

def update_product(product_id: int, product: ProductBase, db: db_dependency):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id '{product_id}' not found")
    
    if product.productName != db_product.productName:
        db_check = db.query(Product).filter(Product.productName == product.productName).first()
        if db_check and db_check.id != product_id and db_check.is_active:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product name'{product.productName}' is already assigned to another product.")


    db_product.productName = product.productName
    db_product.price = product.price
    db_product.stockQty = product.stockQty
    db_product.categoryId = product.categoryId

    try:
        db.commit()
        return {"message": f"Product with id {product_id} updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def delete_product(product_id: int, db: db_dependency):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id '{product_id}' not found")
    db_product.is_active = False
    db.commit()
    return {"message": f"Product with id {product_id} deleted successfully."}
