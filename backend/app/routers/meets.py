from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from aiomysql.connection import Connection
from ..database import Database
from ..database.meets import addMeet, userMeets, doctorMeets

meet_router = APIRouter()


@meet_router.post("")
async def create_meet(user_id: str = Body(...), doctor_id: str = Body(...), conn: Connection = Depends(Database.get_db)):
    await addMeet(user_id, doctor_id, conn)

    return JSONResponse(content="Success", status_code=status.HTTP_201_CREATED)


@meet_router.get("/u/{user_id}")
async def user_meets(user_id: str, conn: Connection = Depends(Database.get_db)):
    doc_ids = await userMeets(user_id, conn)

    return JSONResponse(content=doc_ids, status_code=status.HTTP_200_OK)


@meet_router.get("/d/{doc_id}")
async def doctor_meets(doc_id: str, conn: Connection = Depends(Database.get_db)):
    user_ids = await doctorMeets(doc_id, conn)

    return JSONResponse(content=user_ids, status_code=status.HTTP_200_OK)
