from fastapi import APIRouter, UploadFile, Body, Depends, status
from fastapi.responses import JSONResponse
from ..models.reports import Report
from aiomysql.connection import Connection
from ..database import Database
from ..database.reports import makeReport, getReportById
from ..utils.classify_disease import classify, disease_inference
import datetime


report_router = APIRouter()


@report_router.post("")
async def generate_report(xray: UploadFile, user_id: str = Body(...), conn: Connection = Depends(Database.get_db)):

    img_id = f"UR_{datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.png"
    with open(f"app/static/images/{img_id}", 'wb') as file:
        pic_data = await xray.read()
        file.write(pic_data)

    disease = await classify(img_id)

    report = Report(title=disease, user_id=user_id, image_id=img_id)

    if disease != "No Finding":
        report.description = disease_inference[disease]["description"]
        report.symptoms = disease_inference[disease]["symptoms"]
        report.treatment = disease_inference[disease]["treatment"]

    id = await makeReport(report, conn)
    report = report.dict()
    report["id"] = id

    return JSONResponse(content=report, status_code=status.HTTP_200_OK)


@report_router.get("/{id}")
async def report_id(id: str, conn: Connection = Depends(Database.get_db)):
    report_data = await getReportById(id, conn)

    return JSONResponse(content=report_data, status_code=status.HTTP_200_OK)
