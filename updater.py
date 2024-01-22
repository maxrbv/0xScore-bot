import asyncio

from models.config import read_yaml_file
from pgsql_service.database import PgsqlManager
from utils.target_logger import get_logger
from parsers.parse_xscore import ZeroXScoreParser


cfg = read_yaml_file()
logger = get_logger(name="0xScore parser", session_id="0xScore parser")

pgsql_manager = PgsqlManager(cfg=cfg, logger=logger)
zeroxscore_parser = ZeroXScoreParser(cfg=cfg, logger=logger, pgsql_manager=pgsql_manager)


async def main():
    await pgsql_manager.init()
    await zeroxscore_parser.infinite_parse()


if __name__ == "__main__":
    asyncio.run(main())
