from aiomysql.connection import Connection
from ..models.reports import Report


async def makeReport(report: Report, conn: Connection):
    async with conn.cursor() as cursor:
        try:
            await cursor.execute("""INSERT INTO reports 
                                    (title, description, symptoms, treatment, user_id, image_id)
                                    VALUES (%s, %s, %s, %s, %s, %s)""",
                                 (report.title, report.description, report.symptoms, report.treatment, report.user_id, report.image_id))
            await conn.commit()
            id = cursor.lastrowid
            await cursor.close()
        except Exception as err:
            print(err)

    return id


async def getReportById(id: str, conn: Connection):
    async with conn.cursor() as cursor:
        try:
            await cursor.execute("""SELECT * FROM reports WHERE id = %s""",
                                 (id))
            report_data = await cursor.fetchone()

            await cursor.close()
        except Exception as err:
            print(err)

    return report_data
