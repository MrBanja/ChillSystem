"""Router for telegram bot handling."""
import logging
import json

import aio_pika

import config

from utilites.telegram_bot.data_models import UpdateModel, MessageModel
from utilites.telegram_bot.bot import TBot
from utilites.redis_util import create_redis_pool, Redis


logger = logging.getLogger(__name__)

bot = TBot(token=config.settings.telegram_bot_token)


@bot.process_command(regex=r'^(https://)?(www.)?(youtu.be|youtube.com)')
async def t_bot_add_youtube_url_to_queue(msg: MessageModel):
    """
    Handle youtube video urls sent to bot.

    Add video url to user's queue.
    """
    logger.info(f'User[{msg.from_.id}] send youtube link -- {msg.text}')

    async with create_redis_pool() as redis:
        redis: Redis

        # TODO: Add regex for fetching video id
        video_id = msg.text[17:]
        youtube_url = f'https://www.youtube.com/embed/{video_id}?autoplay=1'

        res = await redis.lpush(msg.from_.id, youtube_url)

        logger.info('Add video to queue.')

        await bot.send_message(f'Nice video, bro! {res} videos in queue', chat_id=msg.chat.id)


@bot.process_command(command='list')
async def t_bot_get_youtube_urls_from_queue(msg: MessageModel):
    """
    Handle `/list` bot command.

    Show all youtube videos queue for user.
    """
    logger.info(f'User[{msg.from_.id}] send `list` command')

    async with create_redis_pool() as redis:
        redis: Redis

        queue_len = await redis.llen(msg.from_.id)
        resp = await redis.lrange(msg.from_.id, 0, queue_len, encoding='utf-8')

        await bot.send_message(f'{resp}', msg.chat.id)


@bot.process_command(command='skip')
async def t_bot_skip_video(msg: MessageModel):
    """
    Handle `/skip` bot command.

    Skip video to next one.
    """
    logger.info(f'User[{msg.from_.id}] send `skip` command')

    connection = config.MQ_CONNECTIONS.get('TBot')

    if connection is None:
        logger.warning(f'Connection for user[{msg.from_.id}] is not open.')
        return await bot.send_message('You are not logged in at the site.', msg.from_.id)

    channel: aio_pika.Channel = await connection.channel()

    websocket_exchange: aio_pika.Exchange = await channel.declare_exchange(
        'WebSocket',
        aio_pika.ExchangeType.DIRECT,
    )

    message_body = {
        'from': msg.from_.id,
        'command': config.WebSocketWorkerCommands.SKIP.value,
    }
    message_body_json_bytes = json.dumps(message_body).encode('utf-8')
    message = aio_pika.Message(message_body_json_bytes, delivery_mode=aio_pika.DeliveryMode.PERSISTENT)

    await websocket_exchange.publish(message, routing_key='bot-worker')

    logger.info('Send skip command to the worker.')


@bot.process_command(command='clear')
async def t_bot_clear_youtube_urls_from_queue(msg: MessageModel):
    """
    Handle `/clear` bot command.

    Clear all youtube videos queue for user.
    """
    logger.info(f'User[{msg.from_.id}] send `clear` command')

    async with create_redis_pool() as redis:
        redis: Redis

        await redis.delete(msg.from_.id)

        await bot.send_message('Queue cleared!', msg.chat.id)

        logger.info(f'Clear users[{msg.from_.id}] video queue')


async def t_bot_unknown_command(update: UpdateModel):
    """Handle unknown message to the telegram bot."""
    # FIXME: Message could not be in update.
    await bot.send_message('Unknown command', chat_id=update.message.chat.id)
