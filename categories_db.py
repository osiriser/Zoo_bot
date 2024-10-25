import asyncpg
import asyncio

async def populate_categories():
    conn = await asyncpg.connect(database="users",
                                 user="postgres",
                                 host="localhost",
                                 password="kuroishi31!",
                                 port=5432)

    # Заполнение таблицы categories
    categories = [
        ('Cat', 'icons/cat-icon.webp'),
        ('Dog', 'icons/dog-icon.png'),
        ('Hamster', 'icons/hamster-icon.webp'),
        ('Bird', 'icons/bird-icon.png'),
        ('Fish', 'icons/fish-icon.png'),
        ('Horse', 'icons/horse.png')
    ]

    for name, image_url in categories:
        await conn.execute("""
            INSERT INTO categories (name, image_url) VALUES ($1, $2)
        """, name, image_url)

    print("Таблица categories успешно заполнена.")

    await conn.close()

# Запуск функции
asyncio.run(populate_categories())
