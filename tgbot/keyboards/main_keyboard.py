from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.callbacks.main_callback import MainCallback


KEYBOARD_UPDATES = "Upcoming updates"
KEYBOARD_QUESTS = "Ongoing quests"


def keyboard_main_builder():
    builder = InlineKeyboardBuilder()
    builder.button(text=KEYBOARD_QUESTS, callback_data=MainCallback(type="ongoing_quests"))
    builder.button(text=KEYBOARD_UPDATES, callback_data=MainCallback(type="updates"))
    return builder.as_markup()
