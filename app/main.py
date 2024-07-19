# initializes the FastAPI application
from fastapi import FastAPI, status, Depends, HTTPException, Request, Form, Query
from fastapi.templating import Jinja2Templates

from .database import engine, Base
from fastapi.staticfiles import StaticFiles
from .routers.api_routes.products import router as product_api_routers
from .routers.api_routes.categories import router as category_api_routers
from .routers.html_routes.products import router as product_html_routers

app = FastAPI()

Base.metadata.create_all(bind=engine)

# adding this line if css, javaScript is needed
# app.mount("static", StaticFiles(directory="/app/static"), name="static")

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

app.include_router(product_api_routers)

app.include_router(category_api_routers)

app.include_router(product_html_routers)

# app.include_router(categories)

# app.include_router(routes.html_routes)