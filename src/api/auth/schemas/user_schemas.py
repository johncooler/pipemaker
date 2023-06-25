from pydantic import BaseModel


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str


class User(BaseModel):
    id: int

    class Config:
        orm_mode = True
