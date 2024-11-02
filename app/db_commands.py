import asyncpg
import os.path
import requests

async def connect():
    return await asyncpg.connect(database="users",
                                 user="postgres",
                                 host="localhost",
                                 password="kuroishi31!",
                                 port=5432)


async def register_user(telegram_id, args, tg_username):
    conn = await connect()
    referral_id = int(args)
    user = await conn.fetchrow("SELECT tg_user_id FROM users WHERE tg_user_id = $1", telegram_id)


    if user is None:
        await conn.execute("""
            INSERT INTO users (tg_user_id, referral_id, tg_username) VALUES ($1, $2, $3)
        """, telegram_id, referral_id, tg_username)

        await conn.close()
        return False
    else:
        await conn.close()
        return True


async def select_user(telegram_id):
    conn = await connect()
    user = await conn.fetchrow("SELECT tg_user_id FROM users WHERE tg_user_id = $1", telegram_id)

    if user is None:
        await conn.close()
        return False
    else:
        await conn.close()
        return True




async def check_args(args, user_id: int):

    if args is not None and await select_user(int(args)) is True and await select_user(user_id) is False:
        return args
    else:
        args = 0
        return args

async def get_user_points(telegram_id):
    conn = await connect()
    points = await conn.fetchval("SELECT number_points FROM users WHERE tg_user_id = $1", telegram_id)
    await conn.close()
    return points

async def update_user_points(telegram_id, points):
    conn = await connect()
    await conn.execute("UPDATE users SET number_points = $1 WHERE tg_user_id = $2", points, telegram_id)
    await conn.close()


async def complete_task(telegram_id, task_id):
    conn = await connect()
    query = f"UPDATE users SET {task_id} = TRUE WHERE tg_user_id = $1"
    await conn.execute(query, telegram_id)
    await conn.execute("""
        UPDATE users
        SET number_points = number_points + 1000
        WHERE tg_user_id = $1
    """, telegram_id)
    await conn.close()

async def get_tasks_status(telegram_id):
    conn = await connect()
    
    # Выполняем запрос к базе данных, чтобы получить состояние задач пользователя
    query = """
    SELECT task1, task2, task3, task4
    FROM users
    WHERE tg_user_id = $1
    """
    
    row = await conn.fetchrow(query, telegram_id)
    
    # Закрываем соединение
    await conn.close()
    
    # Формируем объект с флагами выполнения задач
    tasks_status = {
        "task1": row['task1'],
        "task2": row['task2'],
        "task3": row['task3'],
        "task4": row['task4']
    }
    
    return tasks_status

async def get_categories():
    conn = await connect()
    rows = await conn.fetch("SELECT id, name, image_path FROM categories")
    await conn.close()
    categories = [{"id": row["id"], "name": row["name"], "image_path": row["image_path"]} for row in rows]
    return categories

async def get_subcategories(category_id):
    conn = await connect()
    rows = await conn.fetch("SELECT id, name, image_path FROM subcategories WHERE category_id = $1", int(category_id))
    await conn.close()
    subcategories = [{"id": row["id"], "name": row["name"], "image_path": row["image_path"]} for row in rows]
    return subcategories

async def get_products(subcategory_id):
    conn = await connect()
    rows = await conn.fetch("SELECT id, name, image_path FROM products WHERE subcategory_id = $1", int(subcategory_id))
    await conn.close()
    products = [{"id": row["id"], "name": row["name"], "image_path": row["image_path"]} for row in rows]
    return products


async def add_category(name, image_path):
    conn = await connect()
    query = "INSERT INTO categories (name, image_path) VALUES ($1, $2)"
    await conn.execute(query, name, image_path)
    await conn.close()

async def add_subcategory(name, image_path, category_id):
    conn = await connect()
    query = "INSERT INTO subcategories (name, image_path, category_id) VALUES ($1, $2, $3)"
    await conn.execute(query, name, image_path, category_id)
    await conn.close()

async def add_product(category_id, subcategory_id, name, price, image_path, image_path2, image_path3, description):
    conn = await connect()
    query = """
        INSERT INTO products (name, image_path, image_path2, image_path3, price, description, category_id, subcategory_id)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    """
    await conn.execute(query, name, image_path, image_path2, image_path3, price, description, category_id, subcategory_id)
    await conn.close()

async def get_categories_without_path():
    conn = await connect()
    rows = await conn.fetch("SELECT id, name FROM categories")
    await conn.close()
    categories = [{"id": row["id"], "name": row["name"]} for row in rows]
    return categories

async def get_subcategories_without_path():
    conn = await connect()
    rows = await conn.fetch("SELECT id, name FROM subcategories")
    await conn.close()
    subcategories = [{"id": row["id"], "name": row["name"]} for row in rows]
    return subcategories