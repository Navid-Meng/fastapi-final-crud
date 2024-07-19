# from fastapi import FastAPI, status, Depends, HTTPException, Request, Form, Query
# import models
# from database import engine, SessionLocal
# from pydantic import BaseModel
# from sqlalchemy.orm import Session, Query as SAQuery
# from typing import Annotated, List, Optional
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import HTMLResponse
# from fastapi_pagination import Page, add_pagination, paginate




# # endpoints for api clients #



# # @app.get('/api/products/{product_id}', status_code=status.HTTP_200_OK)
# # async def read_products(product_id: int, db: db_dependency):
# #     product = db.query(models.Product).filter(models.Product.id == product_id).first()
# #     if not product.is_active:
# #         raise HTTPException(status_code=404, detail="Product not found")
# #     return product





    

    
# @app.put('/api/categories/{category_id}', status_code=status.HTTP_200_OK)
# async def update_category(db: db_dependency, category_id: int, new_category_name: str):
#     db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
#     if db_category is None:
#         raise HTTPException(f"Category with id {category_id} not found")
#     db_category.categoryName = new_category_name
#     db.add(db_category)
#     db.commit()
#     return {"message": f"Category with id {category_id} updated successfully"}
