from sqlalchemy.orm import Session

from .models import User
from .schemas.user_schemas import UserCreate
from .hasher import Hasher


def get_user_by_login(db: Session, login: str):
    return db.query(User).filter(User.login == login).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = Hasher.hash_password(user.password)
    user = User(login=user.login, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
