import asyncpg

async def create_table():
    conn = await asyncpg.connect(database="users",
                                 user="postgres",
                                 host="localhost",
                                 password="kuroishi31!",
                                 port=5432)


    await conn.execute("""
                        DROP TABLE IF EXISTS categories;
                        CREATE TABLE categories (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            image_url VARCHAR(255)  -- путь к изображению категории
                        );
                    """)
    
    await conn.execute("""
                        DROP TABLE IF EXISTS subcategories;
                        CREATE TABLE subcategories (
                            id SERIAL PRIMARY KEY,
                            category_id INT REFERENCES categories(id),
                            name VARCHAR(255) NOT NULL
                        );
                    """)

    await conn.execute("""
                        DROP TABLE IF EXISTS products;
                        CREATE TABLE products (
                            id SERIAL PRIMARY KEY,
                            subcategory_id INT REFERENCES subcategories(id),
                            name VARCHAR(255) NOT NULL,
                            price DECIMAL(10, 2),
                            image_url VARCHAR(255)  -- путь к изображению товара
                        );
                    """)

    await conn.close()

import asyncio
asyncio.run(create_table())