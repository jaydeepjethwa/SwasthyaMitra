from aiomysql.connection import Connection
from ..models.ngos import NGO, NGOLogin


async def addNgo(ngo: NGO, conn: Connection):
    async with conn.cursor() as cursor:
        try:
            await cursor.execute("""SELECT * FROM ngos WHERE email = %s""", (ngo.email))
            ngo_data = await cursor.fetchone()
            if ngo_data:
                await cursor.close()
                return None

            await cursor.execute("""INSERT INTO ngos 
                                    (name, email, password, address)
                                    VALUES (%s, %s, %s, %s)""",
                                 (ngo.name, ngo.email, ngo.password, ngo.address))
            await conn.commit()

            await cursor.execute("""SELECT id, name, email, address FROM ngos WHERE email = %s""", (ngo.email))
            ngo_data = await cursor.fetchone()

        except Exception as err:
            print(err)

        await cursor.close()

    return ngo_data


async def ngoLogin(ngo: NGOLogin, conn: Connection):
    async with conn.cursor() as cursor:
        try:
            await cursor.execute("""SELECT * FROM ngos WHERE email = %s""", (ngo.email))
            ngo_data = await cursor.fetchone()

        except Exception as err:
            print(err)

        await cursor.close()

    return ngo_data
