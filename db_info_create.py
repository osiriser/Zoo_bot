import asyncpg

async def create_table():
    conn = await asyncpg.connect(database="users",
                                 user="postgres",
                                 host="localhost",
                                 password="kuroishi31!",
                                 port=5432)


    await conn.execute("""
                       DROP TABLE IF EXISTS bot_info;
                       CREATE TABLE bot_info (
                            task_id SERIAL PRIMARY KEY,
                            description TEXT,
                            link TEXT
                        );
                    """)

    await conn.close()

import asyncio
asyncio.run(create_table())