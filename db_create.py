import asyncpg

async def create_table():
    conn = await asyncpg.connect(database="users",
                                 user="postgres",
                                 host="localhost",
                                 password="kuroishi31!",
                                 port=5432)


    await conn.execute("""
                       DROP TABLE IF EXISTS users;
                       CREATE TABLE users (
                            tg_user_id BIGINT PRIMARY KEY,  -- Telegram user_id
                            tg_username VARCHAR(255),       -- Telegram username
                            referral_id BIGINT,
                            number_points INTEGER NOT NULL DEFAULT 0,
                            country VARCHAR(255),           -- Страна
                            region VARCHAR(255),            -- Регион
                            mobile_number VARCHAR(20),      -- Мобильный номер
                            street_house VARCHAR(255),      -- Улица, дом и корпус
                            zip_code VARCHAR(10),           -- Почтовый индекс
                            extra_info TEXT                 -- Дополнительная информация
                        );
                    """)

    await conn.close()

import asyncio
asyncio.run(create_table())