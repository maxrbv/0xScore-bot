from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode

from tgbot.messages.messages import START_MESSAGE, UPDATES_MESSAGE, create_quest_message
from tgbot.keyboards.main_keyboard import keyboard_main_builder
from tgbot.callbacks.main_callback import MainCallback
from updater import pgsql_manager

user_router = Router(name='default user router')


async def check_user(user_id: int, user_name: str | None):
    user = await pgsql_manager.get_user_by_id(user_id=user_id)
    if not user:
        await pgsql_manager.add_user_info({'user_id': user_id, 'user_name': user_name})
        await pgsql_manager.add_user_interaction({'user_id': user_id, 'action': 'register'})


@user_router.message(CommandStart())
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    await check_user(user_id=user_id, user_name=user_name)
    await message.answer(text=START_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=keyboard_main_builder())


@user_router.message(Command('updates'))
async def updates_command(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    await check_user(user_id=user_id, user_name=user_name)
    await pgsql_manager.add_user_interaction({'user_id': user_id, 'action': 'updates'})
    await message.answer(text=UPDATES_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=keyboard_main_builder())


@user_router.message(Command('ongoing_quests'))
async def ongoing_quests_command(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    await check_user(user_id=user_id, user_name=user_name)
    await pgsql_manager.add_user_interaction({'user_id': user_id, 'action': 'ongoing_quests'})
    ongoing_quests = await pgsql_manager.get_ongoing_quests()
    for quest in ongoing_quests:
        await message.answer(text=create_quest_message(quest), parse_mode=ParseMode.MARKDOWN_V2)


@user_router.callback_query(MainCallback.filter(F.type == "updates"))
async def updates_callback(query: types.CallbackQuery):
    await query.answer()
    user_id = query.from_user.id
    user_name = query.from_user.username
    await check_user(user_id=user_id, user_name=user_name)
    await pgsql_manager.add_user_interaction({'user_id': user_id, 'action': 'updates'})
    await query.message.answer(text=UPDATES_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=keyboard_main_builder())


@user_router.callback_query(MainCallback.filter(F.type == "ongoing_quests"))
async def ongoing_quests_callback(query: types.CallbackQuery):
    await query.answer()
    user_id = query.from_user.id
    user_name = query.from_user.username
    await check_user(user_id=user_id, user_name=user_name)
    ongoing_quests = await pgsql_manager.get_ongoing_quests()
    await pgsql_manager.add_user_interaction({'user_id': user_id, 'action': 'ongoing_quests'})
    for quest in ongoing_quests:
        await query.message.answer(text=create_quest_message(quest), parse_mode=ParseMode.MARKDOWN_V2)
