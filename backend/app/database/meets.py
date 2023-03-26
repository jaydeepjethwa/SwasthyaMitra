from aiomysql.connection import Connection


async def addMeet(user_id: str, doctor_id: str, conn: Connection):
    async with conn.cursor() as cursor:
        try:
            await cursor.execute("""INSERT INTO meets (user_id, doctor_id) 
                                    VALUES (%s, %s)""",
                                 (user_id, doctor_id))

            await conn.commit()
            await cursor.close()

        except Exception as err:
            print(err)


async def userMeets(user_id: str, conn: Connection):
    async with conn.cursor() as cursor:
        try:
            await cursor.execute("""SELECT id, name, email, speciality, address FROM meets, doctors WHERE meets.user_id = %s AND meets.doctor_id = doctors.id""", (user_id))
            doc_ids = await cursor.fetchall()

        except Exception as err:
            print(err)

        await cursor.close()

    return doc_ids


async def doctorMeets(doc_id: str, conn: Connection):
    async with conn.cursor() as cursor:
        try:
            await cursor.execute("""SELECT id, name, email, picture FROM meets, users WHERE meets.doctor_id = %s AND meets.user_id = users.id""", (doc_id))
            user_ids = await cursor.fetchall()

        except Exception as err:
            print(err)

        await cursor.close()

    return user_ids
