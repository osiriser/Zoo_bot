import asyncpg
import asyncio

async def create_table():
    conn = await asyncpg.connect(database="users",
                                 user="postgres",
                                 host="localhost",
                                 password="kuroishi31!",
                                 port=5432)

    # Удаление и создание таблицы categories
    await conn.execute("""
                        DROP TABLE IF EXISTS categories CASCADE;
                        CREATE TABLE categories (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            image_url VARCHAR(255)  -- путь к изображению категории
                        );
                    """)

    # Удаление и создание таблицы subcategories
    await conn.execute("""
                        DROP TABLE IF EXISTS subcategories CASCADE;
                        CREATE TABLE subcategories (
                            id SERIAL PRIMARY KEY,
                            category_id INT REFERENCES categories(id),
                            name VARCHAR(255) NOT NULL,
                            image_url VARCHAR(255)
                        );
                    """)

    # Удаление и создание таблицы products
    await conn.execute("""
                        DROP TABLE IF EXISTS products CASCADE;
                        CREATE TABLE products (
                            id SERIAL PRIMARY KEY,
                            subcategory_id INT REFERENCES subcategories(id),
                            name VARCHAR(255) NOT NULL,
                            price DECIMAL(10, 2),
                            image_url VARCHAR(255)  -- путь к изображению товара
                        );
                    """)

    await conn.close()

# Запуск функции
asyncio.run(create_table())
