from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here
from .user import User
from .product import Product
from .category import Category
# app/models/__init__.py

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here
from .user import User
from .product import Product
from .category import Category