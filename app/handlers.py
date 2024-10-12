from aiogram import F, Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums.parse_mode import ParseMode

import app.keyboards as kb

router = Router()

import asyncpg

async def connect():
    return await asyncpg.connect(database="users",
                                 user="postgres",
                                 host="localhost",
                                 password="kuroishi31!",
                                 port=5432)

@router.message(CommandStart())
async def command_start_handler(message: Message):
    reply_markup = await kb.start_keyboard()
    user_id = message.from_user.id
    username = message.from_user.username

    conn = await connect()
    # Вставка пользователя в базу данных
    try:
        # Вставка пользователя в базу данных
        await conn.execute("""
            INSERT INTO users (tg_user_id, tg_username)
            VALUES ($1, $2)
            ON CONFLICT (tg_user_id) DO NOTHING;
        """, user_id, username)
    finally:
        await conn.close()
    await message.answer("Hello, user!", reply_markup=reply_markup)
