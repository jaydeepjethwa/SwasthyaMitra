import aiomysql


class Database:
    pool = None

    @classmethod
    async def establish_db_connection(cls):
        try:
            print("Connecting to database")
            cls.pool = await aiomysql.create_pool(
                host="localhost", port=3306, minsize=1, maxsize=1,
                user="root", password="", db="swami",
                cursorclass=aiomysql.cursors.DictCursor
            )

        except Exception as err:
            print(err)

    @classmethod
    async def get_db(cls):
        try:
            print("Sharing the connection")
            async with cls.pool.acquire() as conn:
                yield conn
        except Exception as err:
            print(err)

    @classmethod
    async def close_db_connection(cls):
        print("Closing the connection pool with database")
        cls.pool.close()
        await cls.pool.wait_closed()
