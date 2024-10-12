from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
async def start_keyboard():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Store", web_app=WebAppInfo(url=f"https://appminimall.xyz/"))]])
    return markup