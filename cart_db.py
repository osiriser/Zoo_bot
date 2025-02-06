import asyncpg
import asyncio

async def create_cart():
    conn = await asyncpg.connect(database="users",
                                 user="postgres",
                                 host="localhost",
                                 password="kuroishi31!",
                                 port=5432)

    await conn.execute("""
                            DROP TABLE IF EXISTS cart;
                            CREATE TABLE cart (
                            id SERIAL PRIMARY KEY,
                            user_id BIGINT NOT NULL,
                            product_id INTEGER NOT NULL,
                            product_price INTEGER NOT NULL,
                            product_name VARCHAR(255) NOT NULL,
                            product_image VARCHAR(255),
                            quantity INTEGER DEFAULT 1,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );
                        """)

    await conn.close()
asyncio.run(create_cart())