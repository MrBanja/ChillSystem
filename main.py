"""Main app start point"""
import logging

import config

from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.responses import FileResponse

from bot import router as telegram_api_router
from routers.websockets import router as websocket_router


dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI()
app.debug = config.settings.debug

app.include_router(
    telegram_api_router.router,
    tags=['bot'],
    prefix='/bot',
)
app.include_router(
    websocket_router.router,
    tags=['webSocket'],
    prefix='/webSocket',
)


@app.get("/")
async def get():
    """Return web page for video broadcasting."""
    return FileResponse(path=(config.BASE_DIR / 'templates' / 'video_player.html'))
