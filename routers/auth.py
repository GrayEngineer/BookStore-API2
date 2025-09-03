# #this file is for authentication, all authentication.
import sys
sys.path.append("..")

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext # type: ignore
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError # type: ignore

SECRET_KEY = "ioihuahsdiuya876td87aysd98"
ALGORITHM = "HS256"

oauth_bearer = OAuth2PasswordBearer(tokenUrl="token")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")    

models.Base.metadata.create_all(bind=engine)

# app = FastAPI()
router =APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={401:{"user": "Not authorized"}}
)

class CreateUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users)\
        .filter(models.Users.username == username)\
        .first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user        

def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)    


def get_user_exception():
    return HTTPException(status_code=404, detail="User not found")
  

async def get_current_user(token: str = Depends(oauth_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/")
async def get_all_register_user(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

@router.post("/create/user")
async def register_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = models.Users(
        email=create_user.email,
        username=create_user.username,
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        hashed_password=get_password_hash(create_user.password),
        is_active=True,
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"status": "User created successfully"}

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    
    return {"access_token": token}
