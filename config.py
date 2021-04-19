"""Server-wide configurations."""
import enum
import pathlib
import logging

import aio_pika

from typing import Dict, NewType

from fastapi import WebSocket
from pydantic import BaseSettings

TUserId = NewType('TUserId', int)
BASE_DIR = pathlib.Path('.').parent.resolve()

CONNECTED_WEBSOCKETS: Dict[TUserId, WebSocket] = {}
MQ_CONNECTIONS: Dict[str, aio_pika.Connection] = {}


class WebSocketWorkerCommands(enum.Enum):
    """Possible commands that can be passed to websocket worker."""

    SKIP = 'skip'
    CLOSE_WS_CONNECTION = 'close websocket connection'


class Settings(BaseSettings):
    """Settings fro project loaded from .env file."""

    telegram_bot_token: str
    debug: bool = False
    ngrok_tunnel_address: str = ''

    class Config:
        """Configs fro pydantic BaseSettings."""

        env_file = '.env'


settings = Settings()


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'routers': {
            'level': logging.INFO,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/routers.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'default',
        },
        'bot': {
            'level': logging.INFO,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/bot.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'default',
        },
        'main': {
            'level': logging.INFO,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/main.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'handlers': ['main'],
            'level': logging.INFO,
            'propagate': False,
        },
        'routers': {
            'handlers': ['routers'],
            'level': logging.INFO,
            'propagate': False,
        },
        'routers.bot.bot': {
            'handlers': ['bot'],
            'level': logging.INFO,
            'propagate': False,
        },
    },
}
