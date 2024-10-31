from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
async def start_keyboard():
    #markup = InlineKeyboardMarkup(inline_keyboard=[
        #[InlineKeyboardButton(text="Store", web_app=WebAppInfo(url=f"https://appminimall.xyz/"))]])
    #return markup
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Store", url=f"https://appminimall.xyz/")]])
    return markup


async def admin_keyboard():

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Add a category", callback_data="add_category"),
         InlineKeyboardButton(text="Add a subcategory", callback_data="add_subcategory")],
        [InlineKeyboardButton(text="Add a product", callback_data="add_product")]])
    return markup
