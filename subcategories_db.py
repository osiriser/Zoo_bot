import asyncpg
import asyncio

async def populate_subcategories():
    conn = await asyncpg.connect(database="users",
                                 user="postgres",
                                 host="localhost",
                                 password="kuroishi31!",
                                 port=5432)

    # ID категории "Cat" (замените на фактический ID)
    category_id = 1  

    # Подкатегории для категории "Cat" с путями к изображениям
    subcategories = [
        ('Cat Food', category_id, 'icons/cat-food.png'),
        ('Cat Toys', category_id, 'icons/cat-toy.png'),
        ('Cat Beds', category_id, 'icons/cat-house.png'),
        ('Cat Litter', category_id, 'icons/litter-box.png'),
        ('Cat Accessories', category_id, 'icons/pet-bed.png')
    ]

    for name, cat_id, image_url in subcategories:
        await conn.execute("""
            INSERT INTO subcategories (name, category_id, image_url) VALUES ($1, $2, $3)
        """, name, cat_id, image_url)

    print("Таблица subcategories успешно заполнена для категории 'Cat' с изображениями.")

    await conn.close()

# Запуск функции
asyncio.run(populate_subcategories())
