from aiomysql.connection import Connection
from ..models.doctors import Doctor, DoctorLogin


async def addDoctor(doctor: Doctor, conn: Connection):
    async with conn.cursor() as cursor:
        try:
            await cursor.execute("""SELECT * FROM doctors WHERE email = %s""", (doctor.email))
            doctor_data = await cursor.fetchone()
            if doctor_data:
                await cursor.close()
                return None

            await cursor.execute("""INSERT INTO doctors 
                                    (name, email, password, speciality, address, status, certificate)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                                 (doctor.name, doctor.email, doctor.password, doctor.speciality, doctor.address, doctor.status, doctor.certificate))
            await conn.commit()

            await cursor.execute("""SELECT * FROM doctors WHERE email = %s""",
                                 (doctor.email))
            doctor_data = await cursor.fetchone()

        except Exception as err:
            print(err)

        await cursor.close()

    return doctor_data


async def doctorLogin(doctor: DoctorLogin, conn: Connection):
    async with conn.cursor() as cursor:
        try:
            await cursor.execute("""SELECT * FROM doctors WHERE email = %s""", (doctor.email))
            doctor_data = await cursor.fetchone()

        except Exception as err:
            print(err)

        await cursor.close()

    return doctor_data


async def getDoctors(conn: Connection):
    async with conn.cursor() as cursor:
        try:
            await cursor.execute("""SELECT * FROM doctors""")
            doctors = await cursor.fetchall()

        except Exception as err:
            print(err)

        await cursor.close()

    return doctors
