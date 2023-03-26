from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from ..models.ngos import NGO, NGOLogin
from ..database import Database
from ..database.ngos import addNgo, ngoLogin


ngo_router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@ngo_router.post("/signup")
async def signup(ngo: NGO, conn=Depends(Database.get_db)):

    ngo.password = hash_helper.encrypt(ngo.password)

    ngo_data = await addNgo(ngo, conn)

    if not ngo:  # i.e. user exists
        return JSONResponse(content="NGO with given email id already exist.", status_code=status.HTTP_403_FORBIDDEN)

    return JSONResponse(content=ngo_data, status_code=status.HTTP_201_CREATED)


@ngo_router.post("/login")
async def login(user: NGOLogin, conn=Depends(Database.get_db)):
    ngo_data = await ngoLogin(user, conn)

    if not ngo_data:
        return JSONResponse(content="NGO with given email id doesn't exist.", status_code=status.HTTP_404_NOT_FOUND)

    if not hash_helper.verify(user.password, ngo_data["password"]):
        return JSONResponse(content="Incorrect credentials", status_code=status.HTTP_406_NOT_ACCEPTABLE)

    return JSONResponse(content=ngo_data, status_code=status.HTTP_200_OK)
