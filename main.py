import config

from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse

from routers.telegram_bot import router as telegram_api_router
from routers.telegram_bot.router import bot
from utilites.redis_util import create_redis_pool, Redis


app = FastAPI()

app.include_router(
    telegram_api_router.router,
    tags=['bot'],
    prefix='/bot',
)


@app.get("/")
async def get():
    return FileResponse(path=(config.BASE_DIR / 'templates' / 'video_player.html'))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()

    bot.attach_websocket_to_user(user_id, websocket)

    async with create_redis_pool() as redis:
        redis: Redis

        while True:
            video = await redis.rpop(user_id, encoding='utf-8')

            if video:
                await websocket.send_text(f"{video}")

            resp = await websocket.receive_text()

            if resp == 'exit':
                await websocket.close()
                bot.unattach_websocket_by_user_id(user_id)
                break
