import config
import asyncio

from pprint import pprint

from fastapi import APIRouter, Depends

from routers.telegram_bot.dependencies import verify_telegram_bot_token
from utilites.telegram_bot.data_models import UpdateModel, MessageModel
from utilites.telegram_bot.bot import TBot
from utilites.redis_util import create_redis_pool, Redis


router = APIRouter()

bot = TBot(token=config.settings.telegram_bot_token)


@bot.process_command(regex=r'^(https://)?(www.)?(youtu.be|youtube.com)')
async def t_bot_add_youtube_url_to_queue(msg: MessageModel):
    async with create_redis_pool() as redis:
        redis: Redis

        res = await redis.lpush(msg.from_.id, msg.text)

        await bot.send_message(f'Nice video, bro! {res} videos in queue', chat_id=msg.chat.id)


@bot.process_command(command='list')
async def t_bot_get_youtube_urls_from_queue(msg: MessageModel):
    async with create_redis_pool() as redis:
        redis: Redis

        queue_len = await redis.llen(msg.from_.id)
        resp = await redis.lrange(msg.from_.id, 0, queue_len, encoding='utf-8')

        await bot.send_message(f'{resp}', msg.chat.id)


@bot.process_command(command='clear')
async def t_bot_clear_youtube_urls_from_queue(msg: MessageModel):
    async with create_redis_pool() as redis:
        redis: Redis

        resp = await redis.delete(msg.from_.id)

        await bot.send_message(f'Queue cleared!', msg.chat.id)


async def t_bot_unknown_command(update: UpdateModel):
    # FIXME: Message could not be in update.
    await bot.send_message('Unknown command', chat_id=update.message.chat.id)


@router.on_event("startup")
async def t_bot_set_web_hook():
    url = 'https://b50d45d27b05.ngrok.io'
    url += f'/bot/{config.settings.telegram_bot_token}/webHook'
    print('SET WEBHOOK', await bot.set_web_hook(url))


@router.on_event("shutdown")
async def t_bot_delete_web_hook():
    print('DELETE WEBHOOK', await bot.delete_web_hook())


@router.post(
    '/{telegram_bot_token}/webHook',
    dependencies=[Depends(verify_telegram_bot_token)],
    include_in_schema=False,
)
async def web_hook(update_request: UpdateModel):
    pprint(update_request.dict(exclude_none=True))
    asyncio.create_task(bot.update_handler(update_request, default=t_bot_unknown_command))
