from aiogram import F, Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums.parse_mode import ParseMode

import app.keyboards as kb
import db_commands


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, command: CommandObject):
    user_id = message.from_user.id
    bot = message.bot
    args = command.args
    username = message.from_user.username
    new_args = await db_commands.check_args(args, message.from_user.id)
    response = await db_commands.register_user(message.from_user.id, new_args, username)
    reply_markup = await kb.start_keyboard()
    referral_link = await create_start_link(bot=bot, payload=str(user_id))
    await message.answer(f"Hello, user!"
                         f"\nYour referral link: {referral_link}", reply_markup=reply_markup)
