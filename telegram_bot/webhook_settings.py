"""Router for telegram bot handling."""
import logging
import aio_pika
from aiogram import Bot, Dispatcher
import config

bot = Bot(token=config.settings.telegram_bot_token)
logger = logging.getLogger(__name__)


async def t_bot_set_web_hook(dp: Dispatcher):
    """
    Set telegram webHook on server startup.

    Have sense only when testing with ngrok for example.
    """
    url = config.settings.ngrok_tunnel_address
    await bot.set_webhook(url)

    logger.info('Set telegram webHook')

    connection: aio_pika.Connection = await aio_pika.connect(f"amqp://guest:guest@chill_rabbit/")
    config.MQ_CONNECTIONS['TBot'] = connection

    logger.info('Establish connection to RabbitMQ for telegram bot')


async def t_bot_delete_web_hook(dp: Dispatcher):
    """
    Delete telegram webHook on server shutdown.

    Have sense only when testing with ngrok for example.
    """
    await bot.delete_webhook()
    logger.info('Remove webHook')
