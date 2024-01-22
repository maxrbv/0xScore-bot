import asyncio
from datetime import datetime
from logging import Logger

import aiohttp

from models.config import Config
from pgsql_service.database import PgsqlManager


class ZeroXScoreParser:

    def __init__(self, cfg: Config, logger: Logger, pgsql_manager: PgsqlManager):
        self._cfg = cfg
        self._logger = logger
        self._pgsql_manager = pgsql_manager
        self._base_api_url = "https://api.0xscore.io/v2"
        self._timeout = self._cfg.requests.timeout

    async def infinite_parse(self):
        while True:
            await self._main_loop()

    async def _main_loop(self):
        while True:
            await self._add_new_campaigns()
            await asyncio.sleep(self._timeout)

    async def _add_new_campaigns(self):
        self._logger.info("[ZeroXScoreParser:_add_new_campaigns] - Start parsing campaigns")
        json_data = {
            "offset": 0,
            "limit": 24,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url=f"{self._base_api_url}/points-hub/campaigns", json=json_data) as response:
                response_json = await response.json()

        data = await self._process_campaigns(campaigns_list=response_json)
        await self._pgsql_manager.add_campaign_info(data=data)

    async def _process_campaigns(self, campaigns_list: dict) -> list[dict]:
        campaigns_list = campaigns_list.get("campaigns")
        data = []
        for campaign in campaigns_list:
            data.append(
                {
                    "inner_id": int(campaign.get("id")),
                    "project_name": campaign.get("title"),
                    "image_url": campaign.get("icon_url"),
                    "min_score": int(campaign.get("score_limit")),
                    "reward_points": int(campaign.get("reward_data").get("points")),
                    "winners_count": int(campaign.get("reward_data").get("winners_count")),
                    "reward_text": campaign.get("reward_data").get("custom"),
                    "twitter_url": campaign.get("social").get("twitter_url"),
                    "discord_url": campaign.get("social").get("discord_url"),
                    "site_url": campaign.get("social").get("official_site"),
                    "start_date": datetime.strptime(campaign.get("starts_at"), "%Y-%m-%dT%H:%M:%SZ") if campaign.get("starts_at") else None,
                    "end_date": datetime.strptime(campaign.get("ends_at"), "%Y-%m-%dT%H:%M:%SZ") if campaign.get("ends_at") else None,
                }
            )
        return data
