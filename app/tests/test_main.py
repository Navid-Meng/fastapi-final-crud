from fastapi import Header
from fastapi.testclient import TestClient
from ..main import app
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app import models
from ..database import Base
import pytest

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/my_test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db





# create test tables
@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        yield client
    Base.metadata.drop_all(bind=engine)

def test_create_user_for_access_token(test_client):
    user_data = {
        "username": "navid123",
        "password": "navid234"
    }
    
    response = test_client.post("/auth", json=user_data)
    assert response.status_code == 201

def test_login_for_access_token(test_client):
    user_data = {
        "username": "navid123",
        "password": "navid234"
    }
    response = test_client.post("/auth/token", data=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    return response.json()["access_token"]

def test_create_category(test_client):
    data = {"categoryName": "Drinks"}
    
    response = test_client.post("/api/categories", json=data)
    
    assert response.status_code == 201

def test_read_product(test_client):
    
    token = test_login_for_access_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}
    
    productInfo1 = {
        "productName": "Coca",
        "price": 123,
        "stockQty": 123,
        "categoryId": 1,
        "productCode": "12325"
    }
    
    productResponse1 = test_client.post("/api/products/", json=productInfo1, headers=headers)
    
    assert productResponse1.status_code == 201
    
def test_duplicate_product(test_client):
    token = test_login_for_access_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}
    productInfo1 = {
        "productName": "Coca",
        "price": 123,
        "stockQty": 321,
        "categoryId": 1,
        "productCode": "12345"
    }
    
    response = test_client.post("/api/products/", json=productInfo1, headers=headers)
    
    assert response.status_code == 409
    
def test_productCode_validation(test_client):
    token = test_login_for_access_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}
    productInfo1 = {
        "productName": "Fanta",
        "price": 123,
        "stockQty": 321,
        "categoryId": 1,
        "productCode": "123"
    }
    
    response = test_client.post("/api/products/", json=productInfo1, headers=headers)
    
    assert response.status_code == 400, f"Expect status code 422, got {response.status_code}"