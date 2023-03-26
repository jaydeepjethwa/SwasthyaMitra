from fastapi import APIRouter, Body, UploadFile, Depends, status
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from ..models.users import User, UserLogin
from ..database import Database
from ..database.users import addUser, userLogin
import datetime


user_router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@user_router.post("/signup")
async def signup(picture: UploadFile,
                 name: str = Body(...),
                 email: str = Body(...),
                 password: str = Body(...),
                 conn=Depends(Database.get_db)):

    user = User(name=name, email=email, password=password)

    user.picture = f"U_{datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.png"
    user.password = hash_helper.encrypt(user.password)

    user_data = await addUser(user, conn)

    if not user_data:  # i.e. user exists
        return JSONResponse(content="User with given email id already exist.", status_code=status.HTTP_403_FORBIDDEN)

    with open(f"app/static/images/{user.picture}", 'wb') as file:
        pic_data = await picture.read()
        file.write(pic_data)

    return JSONResponse(content=user_data, status_code=status.HTTP_201_CREATED)


@user_router.post("/login")
async def login(user: UserLogin, conn=Depends(Database.get_db)):
    user_data = await userLogin(user, conn)

    if not user_data:
        return JSONResponse(content="User with given email id doesn't exist.", status_code=status.HTTP_404_NOT_FOUND)

    if not hash_helper.verify(user.password, user_data["password"]):
        return JSONResponse(content="Incorrect credentials", status_code=status.HTTP_406_NOT_ACCEPTABLE)

    return JSONResponse(content=user_data, status_code=status.HTTP_200_OK)
