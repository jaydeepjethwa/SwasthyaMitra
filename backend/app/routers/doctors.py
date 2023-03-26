from fastapi import APIRouter, Body, UploadFile, Depends, status
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from ..models.doctors import Doctor, DoctorLogin
from aiomysql.connection import Connection
from ..database import Database
from ..database.doctors import addDoctor, doctorLogin, getDoctors
import datetime


doctor_router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@doctor_router.post("/signup")
async def signup(certificate: UploadFile,
                 name: str = Body(...),
                 email: str = Body(...),
                 password: str = Body(...),
                 speciality: str = Body(...),
                 address: str = Body(...),
                 available: bool = Body(...),
                 conn: Connection = Depends(Database.get_db)):

    doctor = Doctor(name=name, email=email, password=password,
                    speciality=speciality, address=address, status=available)

    doctor.certificate = f"D_{datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.png"
    doctor.password = hash_helper.encrypt(doctor.password)

    doctor_data = await addDoctor(doctor, conn)

    if not doctor_data:  # i.e. doctor exists
        return JSONResponse(content="Doctor with given email id already exist.", status_code=status.HTTP_403_FORBIDDEN)

    with open(f"app/static/images/{doctor.certificate}", 'wb') as file:
        pic_data = await certificate.read()
        file.write(pic_data)

    return JSONResponse(content=doctor_data, status_code=status.HTTP_201_CREATED)


@doctor_router.post("/login")
async def login(doctor: DoctorLogin, conn: Connection = Depends(Database.get_db)):
    doctor_data = await doctorLogin(doctor, conn)

    if not doctor_data:
        return JSONResponse(content="Doctor with given email id doesn't exist.", status_code=status.HTTP_404_NOT_FOUND)

    if not hash_helper.verify(doctor.password, doctor_data["password"]):
        return JSONResponse(content="Incorrect credentials", status_code=status.HTTP_406_NOT_ACCEPTABLE)

    return JSONResponse(content=doctor_data, status_code=status.HTTP_200_OK)


@doctor_router.get("")
async def all_doctors(conn: Connection = Depends(Database.get_db)):
    doctors = await getDoctors(conn)

    return JSONResponse(doctors, status_code=status.HTTP_200_OK)
