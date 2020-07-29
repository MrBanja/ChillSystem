import pathlib

from pydantic import BaseSettings

BASE_DIR = pathlib.Path('.').parent.resolve()


class Settings(BaseSettings):
    telegram_bot_token: str
    ngrok_tunnel_address: str

    class Config:
        env_file = '.env'


settings = Settings()
