
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
    await callback.message.answer(text="Please send a category name")

@router.message(AddCategoryStates.waiting_for_name)
async def process_waiting_for_name(message: Message, state: FSMContext):
    await state.update_data(waiting_for_name=message.text)
    await state.set_state(AddCategoryStates.waiting_for_photo)
    await message.reply(text="Please send a category photo as file")

@router.message(AddCategoryStates.waiting_for_photo)
async def process_waiting_for_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    name_category = data["waiting_for_name"]
    
    photo = message.document  # Берем фото с наибольшим разрешением
    file_id = photo.file_id
    file = await message.bot.get_file(file_id)
    
    # Получаем исходное расширение файла
    file_extension = file.file_path.split('.')[-1]
    file_path = f"/home/developer/Zoo_bot/icons/{name_category}.{file_extension}"  # Путь с расширением
    file_path_short = f"icons/{name_category}.{file_extension}"
    
    await message.bot.download_file(file.file_path, file_path)
    await state.update_data(image_path=file_path)
    await db_commands.add_category(name_category, file_path_short)
    await message.reply("Success!")
    await state.clear()



@router.callback_query(F.data == 'add_subcategory')
async def add_subcategory_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddSubcategoryStates.waiting_for_category_id)
    await callback.message.answer(text="Please choose a category id and send number")
    categories = await db_commands.get_categories_without_path()
    categories_text = "\n".join([f"{category['id']}. {category['name']}" for category in categories])

    await callback.message.answer(f"List of categories:\n{categories_text}")

@router.message(AddSubcategoryStates.waiting_for_category_id)
async def process_waiting_for_category_id(message: Message, state: FSMContext):
    await state.update_data(waiting_for_category_id=message.text)
    await state.set_state(AddSubcategoryStates.waiting_for_name)
    await message.reply(text="Please send a subcategory name")

@router.message(AddSubcategoryStates.waiting_for_name)
async def process_waiting_for_name_subcategory(message: Message, state: FSMContext):
    await state.update_data(waiting_for_name=message.text)
    await state.set_state(AddSubcategoryStates.waiting_for_photo)
    await message.reply(text="Please send a subcategory photo as file")

@router.message(AddSubcategoryStates.waiting_for_photo)
async def process_waiting_for_photo_subcategory(message: Message, state: FSMContext):
    data = await state.get_data()
    name_subcategory = data["waiting_for_name"]
    category_id = data["waiting_for_category_id"]
    photo = message.document  # Берем фото с наибольшим разрешением
    file_id = photo.file_id
    file = await message.bot.get_file(file_id)
    
    # Получаем исходное расширение файла
    file_extension = file.file_path.split('.')[-1]
    file_path = f"/home/developer/Zoo_bot/icons/{name_subcategory}.{file_extension}"  # Путь с расширением
    file_path_short = f"icons/{name_subcategory}.{file_extension}"
    
    await message.bot.download_file(file.file_path, file_path)
    await state.update_data(image_path=file_path)
    await db_commands.add_subcategory(name_subcategory, file_path_short, int(category_id))
    await message.reply("Success!")
    await state.clear()
