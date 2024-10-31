
from aiogram import F, Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import InputFile
import os
from aiogram import types
import app.keyboards as kb
import app.db_commands as db_commands


router = Router()

class AddCategoryStates(StatesGroup):
    waiting_for_name = State()       # Ожидание названия категории
    waiting_for_photo = State()      # Ожидание фото категории

class AddSubcategoryStates(StatesGroup):
    waiting_for_name = State()       # Ожидание названия подкатегории
    waiting_for_photo = State()      # Ожидание фото подкатегории
    waiting_for_category_id = State()  # Ожидание выбора категории, к которой относится подкатегория

class AddProductStates(StatesGroup):
    waiting_for_name = State()       # Ожидание названия продукта
    waiting_for_photo = State()      # Ожидание фото продукта
    waiting_for_category_id = State()  # Ожидание выбора категории продукта
    waiting_for_subcategory_id = State() # Ожидание выбора подкатегории продукта (опционально)
    waiting_for_price = State()      # Ожидание ввода цены продукта
    waiting_for_description = State()  # Ожидание ввода описания продукта

@router.message(CommandStart())
async def command_start_handler(message: Message, command: CommandObject):
    user_id = message.from_user.id
    bot = message.bot
    args = command.args
    username = message.from_user.username
    new_args = await db_commands.check_args(args, message.from_user.id)
    response = await db_commands.register_user(message.from_user.id, new_args, username)
    admin_kb = await kb.admin_keyboard()
    referral_link = await create_start_link(bot=bot, payload=str(user_id))
    await message.answer(f"Hello, user!"
                         f"\nYour referral link: {referral_link}", reply_markup=admin_kb)


@router.callback_query(F.data == 'add_category')
async def add_category_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddCategoryStates.waiting_for_name)
    await callback.bot.send_message(text="Please send a category name")

@router.message(AddCategoryStates.waiting_for_name)
async def process_waiting_for_name(message: Message, state: FSMContext):
    await state.update_data(waiting_for_name=message.text)
    await state.set_state(AddCategoryStates.waiting_for_photo)
    await message.reply(text="Please send a category photo")

@router.message(AddCategoryStates.waiting_for_photo)
async def process_waiting_for_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    name_category = data["waiting_for_name"]
    
    photo = message.photo[-1]  # Берем фото с наибольшим разрешением
    file_id = photo.file_id
    file = await message.bot.get_file(file_id)
    file_path = f"/home/developer/Zoo_bot/icons/{name_category}.jpg"  # Путь, куда сохраняем

    await photo.download(destination_file=file_path)  # Сохраняем файл
    await state.update_data(image_path=file_path)
    await db_commands.add_category(name_category, file_path)
    await message.reply("Success!")
    await state.clear()