from aiomysql.connection import Connection
from ..models.users import User, UserLogin


async def addUser(user: User, conn: Connection):
    async with conn.cursor() as cursor:
        try:
            await cursor.execute("""SELECT * FROM Users WHERE email = %s""", (user.email))
            user_data = await cursor.fetchone()
            if user_data:
                await cursor.close()
                return None

            await cursor.execute("""INSERT INTO Users 
                                    (name, email, password, picture)
                                    VALUES (%s, %s, %s, %s)""",
                                 (user.name, user.email, user.password, user.picture))
            await conn.commit()

            await cursor.execute("""SELECT id, name, email, picture FROM Users WHERE email = %s""", (user.email))
            user_data = await cursor.fetchone()

        except Exception as err:
            print(err)

        await cursor.close()

    return user_data


async def userLogin(user: UserLogin, conn: Connection):
    async with conn.cursor() as cursor:
        try:
            await cursor.execute("""SELECT * FROM Users WHERE email = %s""", (user.email))
            user_data = await cursor.fetchone()

        except Exception as err:
            print(err)

        await cursor.close()

    return user_data
