from pydantic import BaseModel, EmailStr


class NGOLogin(BaseModel):
    email: EmailStr
    password: str


class NGO(BaseModel):
    name: str
    email: EmailStr
    password: str
    address: str
