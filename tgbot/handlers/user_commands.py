from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode

from tgbot.messages.messages import START_MESSAGE, UPDATES_MESSAGE
from tgbot.keyboards.main_keyboard import keyboard_main_builder
from tgbot.callbacks.main_callback import MainCallback


user_router = Router(name='default user router')


@user_router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(text=START_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=keyboard_main_builder())


@user_router.message(Command('updates'))
async def updates_command(message: types.Message):
    await message.answer(text=UPDATES_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=keyboard_main_builder())


@user_router.callback_query(MainCallback.filter(F.type == "updates"))
async def updates_callback(query: types.CallbackQuery):
    await query.answer()
    await query.message.answer(text=UPDATES_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=keyboard_main_builder())