"""Server-wide configurations."""
import enum
import pathlib

import aio_pika

from typing import Dict, NewType

from fastapi import WebSocket
from pydantic import BaseSettings

TUserId = NewType('TUserId', int)
BASE_DIR = pathlib.Path('.').parent.resolve()

CONNECTED_WEBSOCKETS: Dict[TUserId, WebSocket] = {}
CONNECTIONS_TO_CLOSE: Dict[str, aio_pika.Connection] = {}


class WebSocketWorkerCommands(enum.Enum):
    """Possible commands that can be passed to websocket worker."""

    SKIP = 'skip'
    CLOSE_WS_CONNECTION = 'close websocket connection'


class Settings(BaseSettings):
    """Settings fro project loaded from .env file."""

    debug: bool
    telegram_bot_token: str
    ngrok_tunnel_address: str

    class Config:
        """Configs fro pydantic BaseSettings."""

        env_file = '.env'


settings = Settings()
