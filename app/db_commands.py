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
    query = f"UPDATE users SET {task_id} = TRUE WHERE user_id = $1"
    await conn.execute(query, telegram_id)
    await conn.execute("""
        UPDATE users
        SET number_points = number_points + 1000
        WHERE tg_user_id = $1
    """, telegram_id)
    await conn.close()