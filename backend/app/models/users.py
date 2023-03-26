from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    picture: str = None
