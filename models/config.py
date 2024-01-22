from pathlib import Path

from pydantic import BaseModel
import yaml


YAML_PATH = Path(__file__).parent.parent.resolve() / 'Config.yaml'


class TgBot(BaseModel):
    token: str
    allowed_updates: list


class Requests(BaseModel):
    timeout: int


class Pgsql(BaseModel):
    user: str
    password: str
    host: str
    port: int
    dbname: str


class Config(BaseModel):
    tgbot: TgBot
    requests: Requests
    pgsql: Pgsql


def read_yaml_file() -> Config:
    with open(YAML_PATH, 'r') as file:
        yaml_data = yaml.safe_load(file)
        return Config(**yaml_data)
