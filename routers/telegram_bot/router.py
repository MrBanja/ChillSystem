"""Router for telegram bot handling."""
import logging
import asyncio

import aio_pika

import config

from pprint import pprint

from fastapi import APIRouter, Depends

from routers.telegram_bot.dependencies import verify_telegram_bot_token
from routers.telegram_bot.bot import bot, t_bot_unknown_command
from utilites.telegram_bot.data_models import UpdateModel


logger = logging.getLogger(__name__)

router = APIRouter()


@router.on_event("startup")
async def t_bot_set_web_hook():
    """
    Set telegram webHook on server startup.

    Have sense only when testing with ngrok for example.
    """
    url = config.settings.ngrok_tunnel_address
    url += f'/bot/{config.settings.telegram_bot_token}/webHook'
    await bot.set_web_hook(url)

    logger.info('Set telegram webHook')

    connection: aio_pika.Connection = await aio_pika.connect(f"amqp://guest:guest@youtube_sitter_chill_rabbitmq_1/")
    config.MQ_CONNECTIONS['TBot'] = connection

    logger.info('Establish connection to RabbitMQ for telegram bot')


@router.on_event("shutdown")
async def t_bot_delete_web_hook():
    """
    Delete telegram webHook on server shutdown.

    Have sense only when testing with ngrok for example.
    """
    await bot.delete_web_hook()
    logger.info('Remove webHook')


@router.post(
    '/{telegram_bot_token}/webHook',
    dependencies=[Depends(verify_telegram_bot_token)],
    include_in_schema=False,
)
async def web_hook(update_request: UpdateModel):
    """Accept requests from telegram bot."""
    print('NAME ---- ', __name__)
    message_as_dict = update_request.dict(exclude_none=True)

    logger.info(f'Accepted message from telegram bot.')
    logger.debug(f'{message_as_dict}')

    pprint(message_as_dict)
    asyncio.create_task(bot.update_handler(update_request, default=t_bot_unknown_command))
