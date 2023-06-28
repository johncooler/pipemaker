from sqlalchemy.orm import Session

from . import crud
from .hasher import Hasher


def authenticate_user(login: str, password: str, db: Session):
    user = crud.get_user_by_login(db, login=login)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user
