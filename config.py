"""Server-wide configurations."""
from __future__ import annotations
import enum
import pathlib
import aio_pika

from typing import Dict, NewType
from fastapi import WebSocket
from pydantic import BaseSettings
import loguru
import sys
from loguru import logger

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


def create_logger(debug_status: bool) -> loguru.logger:
    """Create project loggers depending on debug status"""

    if debug_status:
        logger.add(sink=sys.stderr,
                   format='{time} | {level} | {exception} {file.path} {function} '
                          'line:{line} { '
                          'message}',
                   enqueue=True,
                   diagnose=True,
                   catch=True,
                   backtrace=True,
                   filter=lambda record: record['extra'].get('name') == 'debug_logger',
                   level='DEBUG')
        debug_logger = logger.bind(name='debug_logger')
        return debug_logger

    logger.add(sink=sys.stderr,
               format='{time} | {level} | {function} {message}',
               enqueue=True,
               level='INFO',
               filter=lambda record: record['extra'].get('name') == 'production_logger')
    production_logger = logger.bind(name='production_logger')
    return production_logger
