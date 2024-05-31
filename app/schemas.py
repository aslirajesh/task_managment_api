from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    tasks: List[Task] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginForm(BaseModel):
    username: str
    password: str

