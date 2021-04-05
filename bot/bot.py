"""Router for telegram bot handling."""
import logging
import json

import aio_pika

import config

from aiogram import (Bot,
                     types,
                     Dispatcher,
                     filters)
from utilites.redis_util import create_redis_pool, Redis


logger = logging.getLogger(__name__)

bot = Bot(token=config.settings.telegram_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=[r'^(https://)?(www.)?(youtu.be|youtube.com)']))
async def t_bot_add_youtube_url_to_queue(message: types.Message):
    """
    Handle youtube video urls sent to bot.

    Add video url to user's queue.
    """
    logger.info(f'User[{message.chat.id}] send youtube link -- {message.text}')

    async with create_redis_pool() as redis:
        redis: Redis

        # TODO: Add regex for fetching video id
        video_id = message.text[17:]
        youtube_url = f'https://www.youtube.com/embed/{video_id}?autoplay=1'

        res = await redis.lpush(message.chat.id, youtube_url)

        logger.info('Add video to queue.')

        await message.answer(f'Nice video, bro! {res} videos in queue')


@dp.message_handler(commands=['list'])
async def t_bot_get_youtube_urls_from_queue(message: types.Message):
    """
    Handle `/list` bot command.

    Show all youtube videos queue for user.
    """
    logger.info(f'User[{message.chat.id}] send `list` command')

    async with create_redis_pool() as redis:
        redis: Redis

        queue_len = await redis.llen(message.chat.id)
        resp = await redis.lrange(message.chat.id, 0, queue_len, encoding='utf-8')

        await message.answer(f'{resp}')


@dp.message_handler(commands=['skip'])
async def t_bot_skip_video(message: types.Message):
    """
    Handle `/skip` bot command.

    Skip video to next one.
    """
    logger.info(f'User[{message.chat.id}] send `skip` command')

    connection = config.MQ_CONNECTIONS.get('TBot')

    if connection is None:
        logger.warning(f'Connection for user[{message.chat.id}] is not open.')
        return await message.answer('You are not logged in at the site.')

    channel: aio_pika.Channel = await connection.channel()

    websocket_exchange: aio_pika.Exchange = await channel.declare_exchange(
        'WebSocket',
        aio_pika.ExchangeType.DIRECT,
    )

    message_body = {
        'from': message.chat.id,
        'command': config.WebSocketWorkerCommands.SKIP.value,
    }
    message_body_json_bytes = json.dumps(message_body).encode('utf-8')
    data = aio_pika.Message(message_body_json_bytes, delivery_mode=aio_pika.DeliveryMode.PERSISTENT)

    await websocket_exchange.publish(data, routing_key='bot-worker')

    logger.info('Send skip command to the worker.')


@dp.message_handler(commands=['clear'])
async def t_bot_clear_youtube_urls_from_queue(message: types.Message):
    """
    Handle `/clear` bot command.

    Clear all youtube videos queue for user.
    """
    logger.info(f'User[{message.chat.id}] send `clear` command')

    async with create_redis_pool() as redis:
        redis: Redis

        await redis.delete(message.chat.id)

        await bot.send_message('Queue cleared!', message.chat.id)

        logger.info(f'Clear users[{message.chat.id}] video queue')


async def t_bot_unknown_command(message: types.Message):
    """Handle unknown message to the telegram bot."""
    # FIXME: Message could not be in update.
    await message.answer('Unknown command')
