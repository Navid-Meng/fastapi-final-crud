from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext # type: ignore
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ...database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import jwt, JWTError #type: ignore
from ...models.user import User
from ...schemas import user

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

SECRET_KEY = "64c48f37631dac30442b99128b309b1b93e754065fbd24d3ed3ad350fd19077a"
ALGORITHM = "HS256"

# for hasing password
bcrypt_context = CryptContext(schemes=['bcrypt'])
# the tokenURL is where tokens are obtained
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

db_dependency = Annotated[Session, Depends(get_db)]

# /auth/  => user creation endpoint
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: user.CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()

# /auth/token/ => token generation endpoint

@router.post("/token", response_model=user.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}



def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

# Token Creation Function
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user.")
        return {'username': username}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")

@router.get("/protected")
async def read_protected(current_user: user.UserBase = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user['username']}