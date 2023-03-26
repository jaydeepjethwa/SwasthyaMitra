from pydantic import BaseModel, EmailStr


class DoctorLogin(BaseModel):
    email: EmailStr
    password: str


class Doctor(BaseModel):
    name: str
    email: EmailStr
    password: str
    speciality: str
    address: str
    status: bool
    certificate: str = None
