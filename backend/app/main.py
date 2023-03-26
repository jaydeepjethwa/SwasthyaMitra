from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import Database
from .utils import load_model

from .routers import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await Database.establish_db_connection()
    load_model()


@app.on_event("shutdown")
async def shutdown():
    await Database.close_db_connection()


@app.get("/")
async def main():
    return "Welcome to Swasthya Mitra"

app.include_router(user_router, tags=["Users"], prefix="/users")
app.include_router(doctor_router, tags=["Doctors"], prefix="/doctors")
app.include_router(meet_router, tags=["Meets"], prefix="/meets")
app.include_router(ngo_router, tags=["NGOs"], prefix="/ngos")
app.include_router(report_router, tags=["Reports"], prefix="/reports")
