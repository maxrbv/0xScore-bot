import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from models.config import read_yaml_file
from utils.target_logger import get_logger
from tgbot.handlers.user_commands import user_router
from parsers.parse_xscore import ZeroXScoreParser


cfg = read_yaml_file()
logger = get_logger(name='OxScore parser', session_id='0xScore parser')

TOKEN = cfg.tgbot.token
ALLOWED_UPDATES = cfg.tgbot.allowed_updates


dp = Dispatcher()
dp.include_router(user_router)

zeroxscore_parser = ZeroXScoreParser(cfg=cfg, logger=logger)


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=f'0xScoreBot | %(asctime)s | %(levelname)4s | %(message)s', stream=sys.stdout)
    zeroxscore_parser.start()
    asyncio.run(main())
