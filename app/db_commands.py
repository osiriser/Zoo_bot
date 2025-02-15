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

async def add_product(category_id, subcategory_id, waiting_for_name, price, image_path, image_path2, image_path3, description):
    conn = await connect()
    query = """
        INSERT INTO products (name, image_path, image_path2, image_path3, price, description, category_id, subcategory_id)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    """
    await conn.execute(query, waiting_for_name, image_path, image_path2, image_path3, price, description, category_id, subcategory_id)
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
