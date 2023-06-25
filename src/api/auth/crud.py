from sqlalchemy.orm import Session

from . import models
from .schemas import user_schemas
from .hasher import Hasher


def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()


def create_user(db: Session, user: user_schemas.UserCreate):
    hashed_password = Hasher.hash_password(user.password)
    user = models.User(login=user.login, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
