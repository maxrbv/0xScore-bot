import datetime
from logging import Logger

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from models.config import Config
from models.models import Base, Campaign, User, UserInteraction


class PgsqlManager:

    def __init__(self, cfg: Config, logger: Logger):
        self._cfg = cfg
        self._logger = logger
        self._db_uri = f'postgresql+asyncpg://{self._cfg.pgsql.user}:{self._cfg.pgsql.password}@{self._cfg.pgsql.host}:{self._cfg.pgsql.port}/{self._cfg.pgsql.dbname}'
        self._engine = create_async_engine(url=self._db_uri, future=True, echo=False)
        self._session_factory = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)
        self._cur_session = None

    async def init(self):
        self._cur_session = self._session_factory()
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all, checkfirst=True)
        self._logger.info(f'[PgsqlManager:init] - Successfully connected to {self._cfg.pgsql.host}:{self._cfg.pgsql.port} and initialized models')

    async def get_all_campaign_ids(self) -> list:
        try:
            async with self._engine.connect() as connection:
                query = select(Campaign.inner_id)
                result = await connection.execute(query)
                campaign_ids = [row[0] for row in result]
                return campaign_ids
        except Exception as e:
            self._logger.error(f"[PgsqlManager:get_all_campaign_ids] - Error retrieving campaign ids from the database: {e}")
            return []

    async def add_campaign_info(self, data: list):
        for row in data:
            try:
                self._cur_session.add(Campaign(**row))
                await self._cur_session.commit()
                self._logger.info(f'[PgsqlManager:add_campaign_info] - Successfully added {row}')
            except Exception as e:
                await self._cur_session.rollback()
                self._logger.error(f'[PgsqlManager:add_campaign_info] - Error adding call record: {e}')

    async def get_ongoing_quests(self) -> list | None:
        try:
            async with self._engine.connect() as connection:
                current_time = datetime.datetime.utcnow()
                query = select(Campaign).where((Campaign.end_date > current_time) | (Campaign.end_date == None))
                result = await connection.execute(query)
                ongoing_quests = [row for row in result]
                ongoing_quests = [Campaign(*row) for row in ongoing_quests]
                return ongoing_quests
        except Exception as e:
            self._logger.error(f"f'[PgsqlManager:get_ongoing_quests] - Error retrieving ongoing quests from the database: {e}")
            return None

    async def get_user_by_id(self, user_id: int) -> list | None:
        try:
            async with self._engine.connect() as connection:
                query = select(User).where(User.user_id == user_id)
                result = await connection.execute(query)
                user = [row for row in result]
                return user
        except Exception as e:
            self._logger.error(f"[PgsqlManager:get_user_by_id] - Error retrieving user by ID from the database: {e}")
            return None

    async def add_user_info(self, user_data: dict):
        try:
            async with self._session_factory() as session:
                new_user = User(**user_data)
                session.add(new_user)
                await session.commit()
                self._logger.info(f'[PgsqlManager:add_user_info] - Successfully added user: {user_data}')
        except Exception as e:
            self._logger.error(f'[PgsqlManager:add_user_info] - Error adding user: {e}')

    async def add_user_interaction(self, interaction_data: dict):
        try:
            async with self._session_factory() as session:
                new_interaction = UserInteraction(**interaction_data)
                session.add(new_interaction)
                await session.commit()
                self._logger.info(f'[PgsqlManager:add_user_interaction] - Successfully added interaction: {interaction_data}')
        except Exception as e:
            self._logger.error(f'[PgsqlManager:add_user_interaction] - Error adding interaction: {e}')
