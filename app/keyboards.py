from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
async def start_keyboard():
    #markup = InlineKeyboardMarkup(inline_keyboard=[
        #[InlineKeyboardButton(text="Store", web_app=WebAppInfo(url=f"https://appminimall.xyz/"))]])
    #return markup
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Store", url=f"https://appminimall.xyz/")]])
    return markup


async def admin_keyboard():
    admin_menu = InlineKeyboardMarkup(row_width=2)
    admin_menu.add(
        InlineKeyboardButton("Add a category", callback_data="add_category"),
        InlineKeyboardButton("Add a subcategory", callback_data="add_subcategory"),
        InlineKeyboardButton("Add a product", callback_data="add_product")
    )