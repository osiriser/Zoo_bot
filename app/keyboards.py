from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
async def start_keyboard():
    #markup = InlineKeyboardMarkup(inline_keyboard=[
        #[InlineKeyboardButton(text="Store", web_app=WebAppInfo(url=f"https://appminimall.xyz/"))]])
    #return markup
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Store", url=f"https://appminimall.xyz/")]])
    return markup