"""Main app start point"""

import config
from config import create_logger
from fastapi import FastAPI
from fastapi.responses import FileResponse

from routers.websockets import router as websocket_router


app = FastAPI()
app.debug = config.settings.debug
logger = create_logger(config.settings.debug)

app.include_router(
    websocket_router.router,
    tags=['webSocket'],
    prefix='/webSocket',
)


@app.get("/")
async def get():
    """Return web page for video broadcasting."""
    logger.debug('Started broadcasting video')
    return FileResponse(path=(config.BASE_DIR / 'templates' / 'video_player.html'))
