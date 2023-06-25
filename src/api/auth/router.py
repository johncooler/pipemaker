from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from session import get_db
from config import settings
from security import create_access_token
from .schemas import user_schemas
from .schemas import token_schemas
from . import crud
from .hasher import Hasher

router = APIRouter()


def authenticate_user(login: str, password: str, db: Session):
    user = crud.get_user_by_login(db, login=login)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/login/", response_model=token_schemas.Token)
def login(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(user.login, user.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"token": access_token, "token_type": "Bearer"}


@router.post("/signup/", response_model=token_schemas.Token)
def signup(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This login already taken")
    crud.create_user(db=db, user=user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"token": access_token, "token_type": "Bearer"}
